package steps;

import client.ApiClient;
import client.TodoApi;
import io.cucumber.java.After;
import io.cucumber.java.Before;
import io.cucumber.java.Scenario;
import io.cucumber.java.en.*;
import io.restassured.response.Response;
import support.ResponseChecks;
import support.ScenarioContext;

import static org.hamcrest.MatcherAssert.assertThat;
import static org.hamcrest.Matchers.*;

public final class ProjectSteps {
    private ScenarioContext context;
    private TodoApi api;
    private Scenario scenario;

    @Before
    public void prepare(Scenario scenario) {
        this.scenario = scenario;
        context = new ScenarioContext();
        api = new TodoApi(new ApiClient(scenario::log));
    }

    @Given("creo un usuario nuevo de prueba")
    public void createUser() {
        Response response = api.createUser(context.email, context.password);
        // Registrar el recurso antes de validar otros campos permite limpiarlo ante fallos.
        Integer id = response.jsonPath().get("Id");
        context.userCreated = id != null && id > 0;
        context.userId = context.userCreated ? id : 0;
        ResponseChecks.success(response);
        response.then().body("Id", greaterThan(0))
                .body("Email", equalTo(context.email))
                .body("FullName", equalTo("API Testing Seccion 2"));
    }

    @And("obtengo su token de autenticacion")
    public void obtainToken() {
        Response response = api.getToken(context.email, context.password);
        ResponseChecks.success(response);
        response.then().body("TokenString", not(blankOrNullString()));
        context.token = response.jsonPath().getString("TokenString");
    }

    @When("creo el proyecto {string} usando el token")
    public void createProject(String name) {
        context.response = api.createProject(name, context.token);
        Integer id = context.response.jsonPath().get("Id");
        context.projectId = id != null ? id : 0;
    }

    @Then("el proyecto creado se llama {string}")
    public void createdProject(String name) {
        assertThat("Identificador del proyecto creado", context.projectId, greaterThan(0));
        ResponseChecks.project(context.response, context.projectId, name, false);
    }

    @And("al consultar el proyecto su nombre es {string}")
    public void readProject(String name) {
        ResponseChecks.project(api.readProject(context.projectId, context.token),
                context.projectId, name, false);
    }

    @When("actualizo el nombre a {string} usando el token")
    public void updateProject(String name) {
        context.response = api.updateProject(context.projectId, name, context.token);
    }

    @Then("el proyecto conserva su identificador y se llama {string}")
    public void updatedProject(String name) {
        ResponseChecks.project(context.response, context.projectId, name, false);
    }

    @When("elimino el proyecto usando el token")
    public void deleteProject() {
        context.response = api.deleteProject(context.projectId, context.token);
        context.projectDeleted = context.response.statusCode() == 200
                && Boolean.TRUE.equals(context.response.jsonPath().getBoolean("Deleted"));
    }

    @Then("el proyecto eliminado se llama {string} y esta marcado como eliminado")
    public void deletedProject(String name) {
        ResponseChecks.project(context.response, context.projectId, name, true);
    }

    @And("el proyecto ya no aparece en la lista de proyectos activos")
    public void projectAbsent() {
        Response response = api.listProjects(context.token);
        response.then().statusCode(200).contentType("application/json")
                .body("$", instanceOf(java.util.List.class))
                .body("Id", not(hasItem(context.projectId)));
    }

    @After
    public void cleanUp() {
        if (!context.userCreated) {
            return;
        }
        try {
            if (context.projectId > 0 && !context.projectDeleted && context.token != null) {
                Response response = api.deleteProject(context.projectId, context.token);
                ResponseChecks.success(response);
                response.then().body("Id", equalTo(context.projectId))
                        .body("Deleted", equalTo(true));
            }
        } finally {
            // Sólo se elimina la cuenta generada en este escenario, incluso si falló el token.
            Response response = api.deleteTestUser(context.userId, context.email, context.password);
            ResponseChecks.success(response);
            response.then().body("Id", equalTo(context.userId));
            scenario.log("Limpieza: usuario temporal eliminado; no se conservan credenciales.");
        }
    }
}
