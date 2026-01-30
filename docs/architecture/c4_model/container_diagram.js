@startuml container_diagram
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Container.puml

Person(user, "WG-Mitglied")

System_Boundary(c1, "ShareShop") {
  Container(ui, "UI", "Vue.js, Vite, Nginx", "SPA")
  Container(api, "API", "FastAPI, Uvicorn", "Schnitstelle die Funktionalitäten der Einkaufsverwaltung zu Verfügung stellt")
  ContainerDb(db, "Datenbank", "SQLAlchemy, MySQL", "Stellt Nutzerdaten sowie deren Einkaufslisten")
}

Rel(user, ui, "ruft über URL im Web-Client auf")
Rel(ui, api, "kommuniziert Nutzereingaben an")
Rel(api, db, "schreibt und liest Daten aus/auf")
@enduml
