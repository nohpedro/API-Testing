package support;

import io.restassured.response.Response;
import java.util.UUID;

/** Instancia exclusiva del escenario: sin estado estático compartido. */
public final class ScenarioContext {
    public final String email = "api." + UUID.randomUUID().toString().replace("-", "") + "@example.com";
    public final String password = "Api!" + UUID.randomUUID();
    public String token;
    public int userId;
    public int projectId;
    public Response response;
    public boolean userCreated;
    public boolean projectDeleted;
}
