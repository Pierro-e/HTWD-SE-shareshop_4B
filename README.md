# Vorlage Projektstruktur & Dokumente

Das Repository enthält die Vorlage einer Projektstruktur und Template-Dokumente
im AsciiDoc-Format. Dies wird für die Bearbeitung der Belegarbeit in Software
Engineering I und II benötigt. Im Detail sind das:

- Projektstruktur anhand
- Templates der benötigten Dokumente (AsciiDoc-Format)
- Vorlage für die Belegabgabe in SE I (AsciiDoc-Format)

**Inhaltsverzeichnis**

- [Projektstruktur](#projektstruktur)
- [Lizenz](#lizenz)

- [Hinweise zu den AsciiDoc-Vorlagen](#hinweise-zu-den-asciidoc-vorlagen)
- [Belegabgabe in SE I](#belegabgabe-in-se-i)

## Projektstruktur

Die Projektstruktur im Verzeichnis **docs** orientiert sich an den wesentlichen Aspekten im Software Engineering und den für die <ins>Abgabe im SE 1 Beleg</ins> geforderten Dokumenten.

```text
docs
├── _includes
│   └── default-attributes.inc.adoc
├── architecture
│   └── architecture_notebook.adoc
├── deployment
├── development
│   └── design.adoc
├── environment
├── project_management
│   └── project_plan.adoc
├── requirements
│   ├── glossary.adoc
│   ├── ux-concept.adoc
│   └── vision.adoc
└── test
    └── test_cases.adoc
```


Im Verzeichnis **belegabgabe_se1** finden Sie die Vorlagedatei
_se1_belegabgabe_t00.adoc_, welche alle Ihre erzeugten Dokumente für die Abgabe
als PDF in <ins>ein</ins> Dokument bündelt.

(Nutzen Sie nicht die Projektvorlage **Projektstruktur_OpenUP-Templates**,
kopieren sie sich die Vorlagedatei _se1_belegabgabe_t00.adoc_ in Ihr
Projektrepository)

Folgende Schritte sind für eine Belegabgabe durchzuführen:

1. Ändern Sie die Themennummer **t00** in der Vorlagedatei
   _se1_belegabgabe_t00.adoc_ in Ihre Themennummer (i01, i02, ..., e01, e02,
   ...).
2. Inhalt der Vorlagedatei anpassen:

   - Ist in Ihrem Projekt in der Datei
     _docs/\_includes/default-attributes.inc.adoc_ der Projektname im Attribut
     `:project-name:` nicht gesetzt bzw. nutzen Sie eine andere Struktur, können
     Sie im Dokumententitel nach dem `:` das `{project-name}` mit Ihrem
     Projektthema ersetzen:

     ```asciidoc
     // --- 1. Projektthema -------------------------
     = SE I - Belegabgabe: {project-name}
     ```

   - Tragen Sie **alle** Teammitglieder als Autoren ein:

     ```asciidoc
     // --- 2. Teammitglieder -----------------------
     Vorname Nachname <s00000@htw-dresden.de>; Vorname Nachname <s00000@htw-dresden.de>; ...
     ```

     > Lange Autorennamen (mehr als 3 Teile) in den Dokumentenattributen müssen
     > mit einem `_` (Unterstrich) zu einer Gruppe von Vor- bzw. Nachnamen
     > zusammengefasst werden. Es treten sonst Formatierungsfehler beim
     > erzeugen der HTML- oder PDF-Dokumente auf. Der `_` (Unterstrich) wird im
     > erzeugten Dokument nicht dargestellt.
     >
     > - `Vorname1_Vorname2 Nachname1_Nachname2 <mail@example.com>`
     > - `Vorname Nachname1_Nachname2_Nachname3 <mail@example.com>`

   - Tragen Sie als Versionsdatum Ihr **Abgabedatum** ein:

     ```asciidoc
     // --- 3. Abgabedatum --------------------------
     01. Januar 2020
     ```

   - Passen Sie bei abweichender Projektstruktur die **include-Pfade** und
     **Dateinamen** zu den einzelnen Dateien (_path/to/file.adoc_) an bzw.
     erweitern Sie es für zusätzliche Dokumente:

     ```asciidoc
     include::path/to/file.adoc[lines=1..1;4..-1,leveloffset=+1]
     ```

     > Beim `include` wird über die `lines=1..1;4..-1` Angabe jeweils die 1.
     > und alles ab der 4. Zeile übernommen. Jedes Dokument ist eigenständig
     > und somit werden über die Zeilen 2 und 3 die jeweiligen Autoren und das
     > Versionsdatum nicht mit übernommen.

3. Erzeugen Sie das Abgabe-PDF _*se1_belegabgabe_t00.pdf*_ ([Hinweise aus dem Praktikum](https://www.informatik.htw-dresden.de/~zirkelba/praktika/se/arbeiten-mit-git-und-asciidoc/praktikumsaufgaben-teil-02.html#_2_generieren_des_ausgabeformates)):

   ```sh
   asciidoctor-pdf se1_belegabgabe_t00.adoc
   ```

   ```sh
   # mit PlantUML
   asciidoctor-pdf -r asciidoctor-diagram se1_belegabgabe_t00.adoc
   ```

   oder:

   ```sh
   asciidoctor -r asciidoctor-pdf -b pdf se1_belegabgabe_t00.adoc
   ```

   ```sh
   # mit PlantUML
   asciidoctor -r asciidoctor-diagram -r asciidoctor-pdf -b pdf se1_belegabgabe_t00.adoc
   ```

4. Prüfen Sie, dass das korrekte **Projektthema**, alle **Teammitglieder** und
   das **Abgabedatum** auf dem Deckblatt stehen und dass ebenfalls alle
   erforderlichen **Dokumente** mit ihren Inhalten enthalten sind.

5. Geben Sie das finale Abgabe-PDF _*se1_belegabgabe_t00.pdf*_ über den
   mitgeteilten Weg ab.

## Lizenz

### Dokumentation

Die Templates im Ordner `docs` und `belegabgabe_se1` unterliegen der
[CC-BY-4.0](https://choosealicense.com/licenses/cc-by-4.0/) Lizenz.

### Quellcode

Aller weitere Quelltexte eingeschlossen Quellcode unterliegen der [MIT Lizenz](https://choosealicense.com/licenses/mit/).
