package client;

import config.Configuration;
import io.restassured.config.HttpClientConfig;
import io.restassured.http.ContentType;
import io.restassured.response.Response;
import io.restassured.specification.RequestSpecification;

import java.util.function.Consumer;

import static io.restassured.RestAssured.given;
import static io.restassured.config.RestAssuredConfig.config;

/** Peticiones nuevas por llamada: sin autenticación global ni logs de secretos. */
public final class ApiClient {
    private final Consumer<String> audit;

    public ApiClient(Consumer<String> audit) {
        this.audit = audit;
    }

    private RequestSpecification request() {
        return given().baseUri(Configuration.BASE_URL)
                .accept(ContentType.JSON).contentType(ContentType.JSON)
                .config(config().httpClient(HttpClientConfig.httpClientConfig()
                        .setParam("http.connection.timeout", Configuration.TIMEOUT_MS)
                        .setParam("http.socket.timeout", Configuration.TIMEOUT_MS)));
    }

    public Response anonymous(String method, String path, Object body) {
        return send(request(), method, path, body, "sin autenticacion");
    }

    public Response basic(String method, String path, String email, String password) {
        return send(request().auth().preemptive().basic(email, password),
                method, path, null, "Basic");
    }

    public Response token(String method, String path, Object body, String token) {
        if (token == null || token.isBlank()) {
            throw new IllegalStateException("No se obtuvo un token valido");
        }
        // Todo.ly espera el encabezado Token, no Authorization: Bearer.
        return send(request().header("Token", token), method, path, body, "Token");
    }

    private Response send(RequestSpecification request, String method, String path,
                          Object body, String authentication) {
        if (body != null) {
            request.body(body);
        }
        Response response = request.when().request(method, path);
        audit.accept(method + " " + path + " | auth=" + authentication
                + " | HTTP " + response.statusCode() + " | " + response.time() + " ms");
        return response;
    }
}
