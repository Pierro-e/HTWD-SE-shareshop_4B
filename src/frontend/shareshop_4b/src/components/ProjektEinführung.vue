<!-- src/components/ProjektEinführung.vue -->
<template>
  <div>
    <h1>ShareShop - Projektstruktur & Start</h1>
    <p>Willkommen im ShareShop Vue-Projekt!</p>

    <section>
      <h2>Was ist eine SPA?</h2>
      <p>
        ShareShop ist eine <strong>Single Page Application (SPA)</strong>. Das bedeutet, die gesamte Anwendung läuft
        auf einer einzigen Webseite, die sich nicht komplett neu lädt. Stattdessen
        lädt die App verschiedene <strong>Komponenten</strong> dynamisch nach und zeigt
        unterschiedliche Inhalte an, ohne die Seite neu zu laden.
      </p>
      <p>
        So wird das Nutzererlebnis schnell, flüssig und fühlt sich wie eine native App an.
      </p>
    </section>

    <section>
      <h2>Wie funktioniert die App?</h2>
      <p>
        Die Hauptkomponente <code>App.vue</code> ruft verschiedene Unter-Komponenten
        auf und steuert, welcher Inhalt gerade angezeigt wird. Zum Beispiel:
      </p>
      <ul>
        <li>Einkaufsliste</li>
        <li>Finanzübersicht</li>
      </ul>
      <p>
        Durch diese Struktur bleibt der Code übersichtlich und modular.
      </p>
    </section>

    <section>
      <h2>Projektstruktur (im src-Ordner)</h2>
      <ul>
        <li><strong>main.js</strong> - Einstiegspunkt, hier wird Vue initialisiert</li>
        <li><strong>App.vue</strong> - Hauptkomponente, hier startet die App</li>
        <li><strong>components/</strong> - Ordner für Unter-Komponenten (z.B. Einkaufslisten, Finanzen)</li>
        <li><strong>assets/</strong> - Bilder, Styles oder andere Ressourcen</li>
        <li><strong>style.css</strong> - Globale CSS-Datei für allgemeine Gestaltung, die auf alle Komponenten wirkt</li>
      </ul>
    </section>

    <section>
      <h2>Was braucht man, um das Projekt auszuführen?</h2>
      <p>
        Um das Projekt lokal zu starten, benötigst du:
      </p>
      <ul>
        <li><strong>Node.js</strong> (Version 14 oder höher) – eine JavaScript-Laufzeitumgebung.  
          Installation: <code>https://nodejs.org</code> (Installer)  
          Update prüfen mit: <code>node -v</code></li>
        <li><strong>npm</strong> (Node Package Manager) – wird zusammen mit Node.js installiert.  
          Update mit: <code>npm install -g npm</code></li>
        <li><strong>Vite</strong> – das Build-Tool und Dev-Server, das im Projekt verwendet wird.  
          Installiert automatisch bei <code>npm install</code> im Projekt, oder manuell mit: <code>npm install -g vite</code>. Überprüfen mit <code>vite --version</code></li>
      </ul>
      <p>Diese Werkzeuge erlauben es dir, die Anwendung zu bauen und lokal im Browser auszuführen.</p>
    </section>

    <section>
      <h2>Wie starte ich die App lokal?</h2>
      <ol>
        <li>Im Projektverzeichnis öffnest du ein Terminal (z.B. in VSCode).</li>
        <li>Du musst dich in diesem Verzeichnis befinden: <code>HTWD-SE-SHARESHOP_4B/src/frontend/shareshop_4b</code></li>
        <li>Führe den Befehl <code>npm install</code> aus, um alle Abhängigkeiten zu installieren.</li>
        <li>Starte den Entwicklungsserver mit <code>npm run dev</code>.</li>
        <li>Öffne dann im Browser die angezeigte Adresse.</li>
        <li>Nach einer Änderung Code speichern -> Änderung wird direkt angezeigt</li>
        <li>Zum Abbrechen / Beenden <code>strg + c</code></li>
      </ol>
      <p>Jetzt kannst du die App live lokal testen und Änderungen werden automatisch aktualisiert.</p>
    </section>
  </div>
</template>

<script></script>

<style></style>