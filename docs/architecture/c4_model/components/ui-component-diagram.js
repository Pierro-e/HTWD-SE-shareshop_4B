@startuml ui-component-diagram
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Container.puml
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Component.puml

Person(user, "WG-Mitglied")

System_Boundary(c1, "ShareShop") {
  Container_Boundary(ui, "UI", "", "", "Singel-Page Anwendung") {
    Component(webClient, "Web Client", "", "rendert angefrage Ressourcen")
    Component(webServer, "Web Server", "", "stellt Ressourcen zur Verfügung")
    Component(userInterface, "User Interface", "", "Ressource")
  }
  Container(api, "API", "", "Schnitstelle die Funktionalitäten der Einkaufsverwaltung zu Verfügung stellt")
  ContainerDb(db, "Datenbank", "", "Stellt Nutzerdaten sowie deren Einkaufslisten")
}

Rel(user, webClient, "interagiert mit")
Rel(webClient, webServer, "fragt nach Ressourcen")
Rel(webServer, userInterface, "liefert an Web Client aus")
Rel(webClient, api, "sendet Anfragen an")
Rel(api, db, "schreibt und holt Daten von")
@enduml
