package support;

import io.restassured.http.ContentType;
import io.restassured.response.Response;

import static io.restassured.module.jsv.JsonSchemaValidator.matchesJsonSchemaInClasspath;
import static org.hamcrest.Matchers.*;

public final class ResponseChecks {
    private ResponseChecks() {}

    public static void success(Response response) {
        response.then().statusCode(200).contentType(ContentType.JSON)
                .body("ErrorCode", nullValue()).body("ErrorMessage", nullValue());
    }

    public static void project(Response response, int id, String name, boolean deleted) {
        success(response);
        response.then().body(matchesJsonSchemaInClasspath("schemas/project.json"))
                .body("Id", equalTo(id))
                .body("Content", equalTo(name))
                .body("Deleted", equalTo(deleted));
    }
}
