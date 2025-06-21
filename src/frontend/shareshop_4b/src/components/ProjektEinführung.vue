<!-- src/components/ProjektEinführung.vue -->
<template>
  <div>
      <h1>ShareShop - Projektstruktur & Start</h1>
    <p>Willkommen im ShareShop Vue-Projekt!</p>

    <button class= "button-edit" @click="$router.push('/settings')">
      Zu den Profileinstellungen
    </button>
    
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
      <h2>Hinweise!</h2>

      <div>
        <h3>Sprachen, die wir in .vue Dateien schreiben.</h3>
        <ul>
          <li><strong>HTML</strong> (mit Vue-Erweiterungen) <strong>im Bereich <code>&lt;template&gt;</code></strong></li>
          <li><strong>Javascript im Bereich <code>&lt;script&gt;</code></strong></li>
          <li><strong>CSS im Bereich <code>&lt;style&gt;</code></strong></li>
        </ul>
      </div>

      <div>
        <h3>Erklärung von zur Funktionalität von App.vue und den Komponenten.</h3>
        <ul>
          <li>Die <code>App.vue</code> ruft die einzelnen Komponenten nur auf.</li>
          <li>Das heißt, dass der wesentliche Code - also Inhalte, Logik und Darstellung - wird in den jeweiligen Komponenten geschrieben.</li>
          <li><strong>App.vue</strong> dient nur als Einstiegspunkt und Strukturgeber für die ganze App.</li>
          <li>Es soll also <strong>so wenig Code wie möglich in der <code>App.vue</code> stehen.</strong></li>
          <li><strong>Hinweis:</strong> das <strong>Dashboard</strong> wird auch in einer eigenen Komponente erstellt (<code>Dashboard.vue</code>) und nicht in der <code>App.vue</code>.</li>
        </ul>
      </div>
    </section>
  </div>
    
</template>

<script></script>

<style></style>