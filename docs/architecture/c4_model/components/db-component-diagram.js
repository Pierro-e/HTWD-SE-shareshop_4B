@startuml db-component-diagram
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Container.puml
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Component.puml

System_Boundary(c1, "ShareShop") {
  Container(ui, "UI", "", "Single-Page Anwendung")
  Container(api, "API", "", "Schnitstelle die Funktionalitäten der Einkaufsverwaltung zu Verfügung stellt")
  Container_Boundary(dbms, "Datenbank", "", "", "verwaltet Daten") {
    Component(dbServer, "Datenbank Server & DBMS")
    Component(db, "Datenbank")
  }
}

Rel(ui, api, "stellt Anfragen an")
Rel(api, dbServer, "bekommt Daten von")
Rel(dbServer, db, "schreibt, liest, verwaltet, ...")
@enduml
