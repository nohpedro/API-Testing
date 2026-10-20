# language: en
@Seccion2 @Regression @Token
Feature: Gestion de proyectos con token en Todo.ly
  Como usuario nuevo de Todo.ly
  quiero gestionar un proyecto con mi token
  para verificar su creacion, actualizacion y eliminacion.

  Scenario: TC-API-001 Crear usuario y gestionar un proyecto con token
    Given creo un usuario nuevo de prueba
    And obtengo su token de autenticacion
    When creo el proyecto "Proyecto Seccion 2" usando el token
    Then el proyecto creado se llama "Proyecto Seccion 2"
    And al consultar el proyecto su nombre es "Proyecto Seccion 2"
    When actualizo el nombre a "Proyecto Seccion 2 actualizado" usando el token
    Then el proyecto conserva su identificador y se llama "Proyecto Seccion 2 actualizado"
    And al consultar el proyecto su nombre es "Proyecto Seccion 2 actualizado"
    When elimino el proyecto usando el token
    Then el proyecto eliminado se llama "Proyecto Seccion 2 actualizado" y esta marcado como eliminado
    And el proyecto ya no aparece en la lista de proyectos activos
