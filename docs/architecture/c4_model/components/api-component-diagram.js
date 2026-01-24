@startuml api-component-diagram
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Container.puml
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Component.puml


System_Boundary(c1, "ShareShop") {
  Container(ui, "UI", "", "Single-Page Anwendung")
  Container_Boundary(api, "API") {
    Component(interface, "die Schnittstelle", "", "stellt Funktionalität")
    Component(asgiServer, "ASGI Server")
  }
  ContainerDb(db, "Datenbank", "", "Stellt Nutzerdaten sowie deren Einkaufslisten")
}

Rel(ui, asgiServer, "stellt Anfragen an")
Rel(interface, asgiServer, "macht zugänglich")
Rel(interface, db, "stellt Transaktionen an")
@enduml
