@startuml system_context_diagram
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Container.puml

Person(user, "WG-Mitglied")
System(system, "ShareShop")

Rel(user, system, "organisert gemeinsame Einkäufe und deren Kostenaufteilung")
@enduml
