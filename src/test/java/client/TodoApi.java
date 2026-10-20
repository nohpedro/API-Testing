package client;

import io.restassured.response.Response;
import java.util.Map;

/** Endpoints y cuerpos de dominio; no contiene aserciones de la prueba. */
public final class TodoApi {
    private final ApiClient client;

    public TodoApi(ApiClient client) {
        this.client = client;
    }

    public Response createUser(String email, String password) {
        return client.anonymous("POST", "/api/user.json", Map.of(
                "Email", email, "Password", password, "FullName", "API Testing Seccion 2"));
    }

    public Response getToken(String email, String password) {
        return client.basic("GET", "/api/authentication/token.json", email, password);
    }

    public Response createProject(String name, String token) {
        return client.token("POST", "/api/projects.json", Map.of("Content", name), token);
    }

    public Response readProject(int id, String token) {
        return client.token("GET", "/api/projects/" + id + ".json", null, token);
    }

    public Response updateProject(int id, String name, String token) {
        return client.token("PUT", "/api/projects/" + id + ".json", Map.of("Content", name), token);
    }

    public Response deleteProject(int id, String token) {
        return client.token("DELETE", "/api/projects/" + id + ".json", null, token);
    }

    public Response listProjects(String token) {
        return client.token("GET", "/api/projects.json", null, token);
    }

    public Response deleteTestUser(int id, String email, String password) {
        return client.basic("DELETE", "/api/user/" + id + ".json", email, password);
    }
}
