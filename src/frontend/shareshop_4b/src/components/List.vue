<template> 
  <AppHeader :title="list_name">
  <template #left>
    <button
      :disabled="showpopup_product || showpopup_list || showpopup_add_member"
      @click="$router.push('/listen')"
      class="button button-cancel back-button"
    >
      <font-awesome-icon icon='arrow-left'/>
    </button>
  </template>

  <template #right>
    <button
      :disabled="showpopup_product || showpopup_list || showpopup_add_member"
      @click="openProductPopup()"
      class="button button-add button-add-header"
    >
      <font-awesome-icon icon='plus'/>
    </button>
  </template>
  </AppHeader>

  <div class="settings-section">
    <div class="settings-container">
      <button
        :disabled="
          showpopup_product || showpopup_list || showpopup_add_member
        "
        @click="openListPopup()"
        class="button button-settings"
      >
        <font-awesome-icon icon='circle-info'/> Info
      </button>
      <button
        :disabled="
          showpopup_product || showpopup_list || showpopup_add_member
        "
        @click="einkauf_abschließen"
        class="button button-submit button-einkauf-tätigen"
      >
        <font-awesome-icon icon='cart-shopping'/> Einkauf
      </button>
      <button @click="list_archive">
        <font-awesome-icon icon='box-archive'/> Archiv
      </button>
    </div>
    <!--
    <div class="buy-container" >
      <button
        :disabled="
          showpopup_product || showpopup_list || showpopup_add_member
        "
        @click="einkauf_abschließen"
        class="button button-submit button-einkauf-tätigen"
      >
        <font-awesome-icon icon='cart-shopping'/> Einkauf
      </button>
    </div>
    -->
  </div>

  <div v-if="loadingActive" class="loading">Laden...</div>
  <div v-if="errorMessage && !showpopup_product && !showpopup_list && !showpopup_add_member" class="error">{{ errorMessage }}</div>
  <div v-if="productNum === 0" class="info">
      Liste leer
    </div>

  <div v-if="showpopup_list" class="popup-overlay">
    <div class="popup-content">
      <h3>Listeninformationen</h3>
      <p>Name der Liste: {{ list_name }}</p>
      <p>Ersteller: {{ list_creator_name }}</p>

      <div v-if="infoMessage" class="success">{{ infoMessage }}</div>
      <div v-if="errorMessage" class="error">{{ errorMessage }}</div>


      <br></br>
      <h4>Mitglieder</h4>
      
      <div
        v-for="mitglied in mitglieder"
        :key="mitglied.id"
        class="mitglieder-anzeige"
      >
        <div>{{ mitglied.name }}</div>
        <button
          v-if="mitglied.id === user.id || user.id === list_creator_id"
          @click="mitglied_entfernen(mitglied.id)"
          class="button button-delete-member"
        >
          {{ mitglied.id === user.id ? 'Verlassen' : 'Entfernen' }}
        </button>
        
      </div>
      
      <button @click="showpopup_list = false" class="button button-cancel">
        Schließen
      </button>
      <button @click="mitglied_hinzufügen_popup()" class="button button-add">
        Mitglied hinzufügen
      </button>
      <button v-if="user.name == list_creator_name" @click="delete_list()" class="button-delete">
        Liste löschen 
      </button>
    </div>
  </div>

  <div v-if="showpopup_product" class="popup-overlay">
    <div class="popup-content">
      <h3>Neues Produkt hinzufügen</h3>
      <div v-if="errorMessage" class="error">{{ errorMessage }}</div>
      <v-select
        v-model="dropdownSelected"
        :options="dropdownOptions"
        taggable
        :clearable="false"
        placeholder="Produkt eingeben..."
        :selectable="option => option.header != true"
        @search="onSearch"
      >
        <template #no-options>
          Keine Favoriten/Vorschläge
        </template>
      </v-select>

      <button @click="cancel_product_popup" class="button button-cancel">
        Abbrechen
      </button>
      <button @click="add_product" class="button button-submit">
        Hinzufügen
      </button>
    </div>
  </div>

  <div v-if="showpopup_add_member" class="popup-overlay">
    <div class="popup-content">
      <h3>Mitglied hinzufügen</h3>
      <input
        class="input"
        v-model="new_member_email"
        type="text"
        placeholder="E-Mail"
        maxlength="30"
      />
      <div v-if="errorMessage" class="error">{{ errorMessage }}</div>
      <button
        @click="cancel_mitglied_hinzufügen"
        class="button button-cancel"
      >
        Abbrechen
      </button>
      <button @click="mitglied_hinzufügen" class="button button-submit">
        Hinzufügen
      </button>
    </div>
  </div>

  <div class="card-grid">
    <ProductCard
      v-for="(product, index) in listenprodukte"
      :key="index"
      :product="product"
      :onSettings="product_settings"
    />
  </div>
  <BottomBar 
    :highlight-btn="1"
  />
  <div
  v-if="showpopup_delete_list_confirm"
  class="popup-overlay"
  @click.self="showpopup_delete_list_confirm = false"
>
  <div class="popup-content">
    <h3>Liste verlassen und löschen</h3>
    <p>
      Diese Liste wird gelöscht, da sie der Ersteller sind.
    </p>
    <p>Möchten Sie die Liste wirklich löschen?</p>

    <div class="button-container">
      <button
        @click="showpopup_delete_list_confirm = false"
        class="button button-cancel"
      >
        Abbrechen
      </button>
      <button
        @click="liste_endgültig_löschen()"
        class="button button-delete"
      >
        Bestätigen und löschen
      </button>
    </div>
  </div>
</div>
    
</template>

<script>
import axios from "axios";
import { inject } from "vue";
import AppHeader from "./AppHeader.vue";
import ProductCard from "./ProductCard.vue";
import BottomBar from "./BottomBar.vue";
export default {
  name: "Liste",
  inject: ["user", "getUser"],
  props: ["list_id"],
  components: {
    AppHeader, 
    ProductCard, 
    BottomBar
  },
  data() {
    return {
      list_name: "",
      list_creator_id: null,
      list_creator_name: "",
      errorMessage: "",
      infoMessage: "",
      productNum: -1,
      loadingActive: true,
      showpopup_product: false,
      showpopup_list: false,
      showpopup_delete_member: false,
      showpopup_add_member: false,
      new_member_email: "",
      new_product: "",
      listenprodukte: [],
      listenprodukte_names: [],
      listenprodukte_einheiten: [],
      mitglieder_ids: [],
      mitglieder: [],
      userData: null, // hier speichern wir den injecteten user
      dropdownSelected: "",
      dropdownOptions: [],
      searchTimeout: 0,
      prevSearchText: "",
      showpopup_delete_list_confirm: false,
    };
  },
  methods: {
    async get_list(id) {
      this.errorMessage = "";
      try {
        const response = await axios.get(
          `http://141.56.137.83:8000/listen/by-id/${id}`,
        );
        this.list_name = response.data.name;
        this.list_creator_id = response.data.ersteller;

        const creator = await this.getUser(this.list_creator_id);
        this.list_creator_name = creator.name || "Unbekannt";
      } catch (error) {
        if (
          error.response &&
          error.response.data &&
          error.response.data.detail
        ) {
          this.errorMessage = error.response.data.detail;
        } else {
          this.errorMessage = "Fehler beim Laden der Liste";
        }
      }
    },

    async get_list_members(id) {
      this.errorMessage = "";
      try {
        const response = await axios.get(
          `http://141.56.137.83:8000/listen/${id}/mitglieder`,
        );
        let mitgliederData = response.data;

        // Wenn response.data kein Array ist, packe es in ein Array (falls einzelnes Objekt)
        if (!Array.isArray(mitgliederData)) {
          mitgliederData = [mitgliederData];
        }

        this.mitglieder = await Promise.all(
          mitgliederData.map(async (mitglied) => {
            try {
              // nutzer_id aus dem Objekt extrahieren
              const user = await this.getUser(mitglied.nutzer_id);
              return {
                id: mitglied.nutzer_id,
                name: user.name || "Unbekannt",
                email: user.email || "Keine E-Mail",
              };
            } catch {
              return {
                id: mitglied.nutzer_id,
                name: "Fehler beim Laden",
                email: "-",
              };
            }
          }),
        );
      } catch (error) {
        if (
          error.response &&
          error.response.data &&
          error.response.data.detail
        ) {
          this.errorMessage = error.response.data.detail;
        } else {
          this.errorMessage = "Fehler beim Laden der Mitglieder";
        }
      }
    },

    async get_products(id) {
      this.errorMessage = "";
      try {
        const response = await axios.get(
          `http://141.56.137.83:8000/listen/${id}/produkte`,
        );
        this.listenprodukte = response.data;

        this.productNum = 0;
        for (const produkt of this.listenprodukte) {
          this.productNum++;
          // produkt_menge formatieren: Wenn Nachkommastellen == 0, als Integer anzeigen
          if (
            produkt.produkt_menge !== undefined &&
            produkt.produkt_menge !== null
          ) {
            const menge = Number(produkt.produkt_menge);
            // Prüfen ob die Zahl eine ganze Zahl ist
            if (Number.isInteger(menge)) {
              produkt.produkt_menge = menge.toString(); // z.B. 5 statt 5.00
            } else {
              // andernfalls auf 2 Nachkommastellen runden (falls notwendig)
              produkt.produkt_menge = menge.toFixed(2);
            }
          }
        }
      } catch (error) {
        if (
          error.response &&
          error.response.data &&
          error.response.data.detail
        ) {
          this.errorMessage = error.response.data.detail;
        } else {
          this.errorMessage = "Fehler beim Laden der Produkte";
        }
      }
      this.loadingActive = false;
    },

    openListPopup() {
      this.errorMessage = "";
      this.showpopup_list = true;
      this.showpopup_product = false;
    },

    async openProductPopup() {
      this.errorMessage = "";
      this.showpopup_product = true;
      this.showpopup_list = false;
      this.dropdownSelected = "";

      this.$nextTick(() => { // warten bis das Popup da ist
        const input = document.getElementsByClassName("vs__search")[0];
        if (input) input.setAttribute("maxlength", 30); // Länge begrenzen von Suchfeld
      });

      this.loadDropdownList(0, "");
    },

    async loadDropdownList(type, searchText){
      this.dropdownOptions = [];
      if (type == 0) { // Bedarfsvorhersage/Favoriten
        try {
          var response = await axios.get(`http://141.56.137.83:8000/bedarfsvorhersage/${this.user.id}`,{
            params: {decayDays: this.userData.decaydays}
          })
          var recommendedProducts = response.data;

          response = await axios.get(`http://141.56.137.83:8000/fav_produkte/nutzer/${this.user.id}`);
          var favoriteProducts = response.data;

          var tempOptions = [];
          if (favoriteProducts.length != 0){
            tempOptions.push({label: "Favoriten", header: true})
            for (const product of favoriteProducts){
              tempOptions.push({label: `${product.produkt_name}`})
            }
          }

          if (recommendedProducts.length != 0){
            tempOptions.push({label: "Vorschläge", header: true})
            for (const product of recommendedProducts){
              tempOptions.push({label: `${product.produkt_name}`})
            }
          }
          
          this.dropdownOptions = tempOptions;
          this.errorMessage = "";
        } catch (error) {
          if (
            error.response &&
            error.response.data &&
            error.response.data.detail
          ) {
            this.errorMessage = error.response.data.detail;
            
          } else {
            this.errorMessage = "Fehler beim Laden von Favoriten/Bedarfsvorhersage";
          } 
        }
      } 
      else if (type == 1) { // Suchvorschläge > mind. 1 Zeichen eingegeben
        try {
          const response = await axios.get(
            `http://141.56.137.83:8000/produkte/suche/`,
            { params: { query: searchText } }
          );
          var suggestions = response.data;
          var tempOptions = [];
          
          for (const product of suggestions){
            tempOptions.push({label: `${product.name}`})
          }

          this.dropdownOptions = tempOptions;
          this.errorMessage = ""
        } catch (error) {
          if (
            error.response &&
            error.response.data &&
            error.response.data.detail
          ) {
            this.errorMessage = error.response.data.detail;
            
          } else {
            this.errorMessage = "Fehler beim Laden der Vorschläge";
          } 
          return;
        }
      }
    },

    async onSearch(searchText){ // aufgerufen, wenn was ins Dropdown eingegeben wird
      clearTimeout(this.searchTimeout);

      if (searchText.length == 0){ // Bedarfsvorhersage/Favoriten
        this.loadDropdownList(0, "");
      }
      else { // Suchvorschläge > mind. 1 Zeichen eingegeben
        if (searchText.length == 1 && this.prevSearchText.length != 2){ // sofort bei erster Eingabe suchen, nicht beim zurücklöschen
          this.loadDropdownList(1, searchText);
        }
        
        this.searchTimeout = setTimeout(() => { // sonst max. jede Sekunde, um Spammen zu verhindern
          this.loadDropdownList(1, searchText);
        }, 1000)
        this.prevSearchText = searchText
      }
    },

    async add_product() {
      const list_id = this.list_id || this.$route.params.id;
      const user_id = this.user.id;

      this.errorMessage = "";
      if (this.dropdownSelected.label){ // aus Suche/Vorschläge
        this.new_product = this.dropdownSelected.label;
      }
      else { // neu eingegeben
        this.new_product = this.dropdownSelected;
      }

      if (this.new_product == "") {
        this.errorMessage = "Produktname darf nicht leer sein";
        return;
      }

      let produkt_Id;
      
      try {
        // Produkt existiert schon?
        const responseCheck = await axios.get(
          `http://141.56.137.83:8000/produkte/by-name/${encodeURIComponent(this.new_product.trim())}`,
        );
        produkt_Id = responseCheck.data.id;
      } catch (error) {
        // Wenn 404 (Produkt nicht gefunden), dann neu anlegen
        if (error.response && error.response.status === 404) {
          try {
            const responseCreate = await axios.post(
              `http://141.56.137.83:8000/produkte_create`,
              {
                name: this.new_product.trim(),
              },
            );
            produkt_Id = responseCreate.data.id;
          } catch (error) {
            if (
              error.response &&
              error.response.data &&
              error.response.data.detail
            ) {
              this.errorMessage = error.response.data.detail;
            } else {
              this.errorMessage = "Fehler beim Anlegen des Produkts"; 
            }
            return;
          }
        }
      }

      if (!list_id || !produkt_Id || !user_id) {
        return;
      }
      
      try {
        await axios.post(
          `http://141.56.137.83:8000/listen/${list_id}/produkte/${produkt_Id}/nutzer/${user_id}`,
        );
        this.errorMessage = "";
      } catch (error) {
        if (error.response) {
          this.errorMessage =
            error.response.data.detail ||
            "Unbekannter Fehler beim Hinzufügen des Produkts zur Liste";
        }
       return;
      }
      
      // ist neues Produkt ein Favorit?
      const response = await axios.get(`http://141.56.137.83:8000/fav_produkte/nutzer/${user_id}`);
      var favoriteProducts = response.data;

      var favFound = false
      var favData = null
      var favID = 0

      for (const product of favoriteProducts){
        if (product.produkt_name === this.new_product.trim()){
          favID = product.produkt_id;
          if (product.menge == null){
            product.menge = 0;
          }
          if (product.einheit_id == null){
            product.einheit_id = 0;
          }

          favData = {
            produkt_menge: product.menge,
            einheit_id: product.einheit_id,
            beschreibung: product.beschreibung,
          }
          favFound = true
          break
        }
      }

      // bei Favorit: Produkt mit Beschreibung, Menge+Einheit updaten!
      if (favFound){
        try {
          await axios.put(
            `http://141.56.137.83:8000/listen/${list_id}/produkte/${favID}/nutzer/${user_id}`,
            favData
          );
        } catch (error) {
          this.errorMessage = error.response?.data?.detail || "Fehler beim Speichern";
          return;
        }
      }

      this.dropdownSelected = "";
      this.new_product = "";
      this.get_products(list_id);
    },

    cancel_product_popup() {
      this.errorMessage = "";
      this.showpopup_product = false;
      this.new_product = "";
      this.dropdownSelected = "";
    },

    mitglied_hinzufügen_popup() {
      this.errorMessage = "";
      this.showpopup_list = false;
      this.showpopup_add_member = true;
    },

    async mitglied_entfernen(mitglied_id) {
      const list_id = this.list_id || this.$route.params.id;
      const requester_id = this.user.id; 
      
      if (requester_id === this.list_creator_id && mitglied_id === requester_id) {
        this.handle_ersteller_verlassen();
        return; 
      }
      try {
        await axios.delete(
          `http://141.56.137.83:8000/listen/${list_id}/mitglieder/${mitglied_id}`,
          {
            params: {
              requesterId: requester_id,
            },
          }
        );
        // nur wenn ersteller andere person entfernt, nicht wenn nicht ertsleller sich selbst entfernt
        if (mitglied_id != requester_id){

        this.infoMessage = "Mitglied erfolgreich entfernt.";
        }
        this.get_list_members(list_id); // Aktualisiere die Mitgliederliste
        this.errorMessage = "";
         setTimeout(() => {
        this.infoMessage = ""; 
        }, 2000);
        
       
      } catch (error) {
        if (
          error.response &&
          error.response.data &&
          error.response.data.detail
        ) {
          this.errorMessage = error.response.data.detail;
        } 
        if (mitglied_id == requester_id && error.response.status != 403) {
            this.get_list_members(list_id); 
          }
        else {
          this.errorMessage = "Fehler beim Entfernen des Mitglieds";
        }
      }
    },

    async mitglied_hinzufügen() {
      this.errorMessage = "";
      const list_id = this.list_id || this.$route.params.id;
      const user_email = this.new_member_email.trim();
      let new_member_id;

      if (!user_email) {
        this.errorMessage = "E-Mail darf nicht leer sein";
        return;
      }

      // email prüfen
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

      if (!emailRegex.test(user_email)) {
        this.errorMessage = "Bitte eine gültige E-Mail-Adresse eingeben!";
        return;
      }

      try {
        const userResponse = await axios.get(
          `http://141.56.137.83:8000/nutzer/by-email`,
          {
            params: { email: user_email },
          },
        );
        new_member_id = userResponse.data.id;
      } catch (error) {
        if (
          error.response &&
          error.response.data &&
          error.response.data.detail
        ) {
          this.errorMessage = error.response.data.detail;
        } else {
          this.errorMessage = "Fehler beim Finden des Nutzers";
          return;
        }
        return;
      }

      try {
        const response = await axios.post(
          `http://141.56.137.83:8000/listen/${list_id}/mitglieder/${new_member_id}`,
        );
        this.showpopup_add_member = false;
        this.errorMessage = "";
        this.new_member_email = "";
        this.get_list_members(list_id); // Aktualisiere die Mitgliederliste
      } catch (error) {
        if (
          error.response &&
          error.response.data &&
          error.response.data.detail
        ) {
          this.errorMessage = error.response.data.detail;
        } else {
          this.errorMessage = "Person bereits Mitglied der Liste.";
        }
        this.showpopup_list = true;
      }
    },

    cancel_mitglied_hinzufügen() {
      this.errorMessage = "";
      this.showpopup_add_member = false;
      this.new_member_email = "";
    },

    product_settings(product) {
      const listenId = this.list_id || this.$route.params.id;
      const listenName = this.list_name;
      const produktId = product.produkt_id;
      const nutzerId = product.hinzugefügt_von;

      this.$router.push({
        name: "ProductDetail",
        params: {
          listenId,
          produktId,
          nutzerId
        },
        query: {
          list_name: listenName
        }
      });
    },


    einkauf_abschließen() {
      if (this.productNum == 0){
        alert("Liste ist leer! Füge Produkte hinzu, um einzukaufen!");
        return;
      }
      const list_id = this.list_id || this.$route.params.id;

      this.$router.push(`/list/${list_id}/einkauf`);
    },

    list_archive() {
      const list_id = this.list_id || this.$route.params.id;
      const list_name = this.list_name;
      this.$router.push({ 
        name: "ListArchive", 
        params: { list_id},
        query: { list_name } 
      });
    },

    async delete_list() {
      if (!confirm("Möchtest du diese Liste wirklich löschen? Alle Daten gehen verloren!")) {
        return;
      }
      this.errorMessage = "";
      this.infoMessage = ""; // Nachricht vor dem Versuch löschen
      
      try {
        // Sicherstellen, dass die ID korrekt verwendet wird
        const list_id = this.list_id || this.$route.params.id;
        await axios.delete(`http://141.56.137.83:8000/listen/${list_id}`);

        // Erfolgsfall (Rückgabe 204 No Content führt hier zur erfolgreichen Ausführung)
        this.infoMessage = "Liste wurde erfolgreich gelöscht!";
        setTimeout(() => {
          this.$router.push("/listen");
        }, 2000);

      } catch (error) {
        console.error("Fehler beim Löschvorgang:", error);
        // zentralistiertte Fehlerbehandlung basierend auf der Backend-Antwort
        if (
          error.response &&
          error.response.status === 404
        ) {
          // Fehlermeldung vom Backend: "Liste nicht gefunden"
          this.errorMessage = error.response.data.detail || "Liste nicht gefunden.";
        } else {
          // Generischer Fehler
          this.errorMessage = "Serverfehler oder unerwarteter Fehler beim Löschen der Liste.";
        }
      }
    },
    handle_ersteller_verlassen() {
      this.showpopup_delete_list_confirm = true;
    }, 
    async liste_endgültig_löschen() {
  const list_id = this.list_id || this.$route.params.id;
  const requester_id = this.user.id;
  
  // Schließe das Popup sofort
  this.showpopup_delete_list_confirm = false;

  try {
    
    await axios.delete(
        `http://141.56.137.83:8000/listen/${list_id}`,
        {
          params: {
            requesterId: requester_id,
          },
        }
    );
    this.infoMessage = "Liste wurde erfolgreich gelöscht.";
    this.errorMessage = "";
    // zur Listenübersicht nach erfolgreicher Löschung
    this.$router.push('/listen');

  } catch (error) {
    this.errorMessage = "Fehler beim Löschen der Liste: " + (error.response?.data?.detail || error.message);
  }
},

  },
  mounted() {
    this.errorMessage = "";
    const id = this.list_id || this.$route.params.id;
    this.get_list(id);
    this.get_list_members(id);
    this.get_products(id);
    // Injected user in data speichern
    this.userData = this.user;
  },
};
</script>

<style scoped>

.button-einkauf-tätigen {
  position: relative;
  margin-top: 0px;
}

/* Settings-Container fixiert unter der Überschrift mittig */
.settings-container {
  background-color: var(--accent-header-bg-color);
  box-shadow: 0 2px 5px var(--box-shadow-color);
  position: fixed;
  top: 70px; /* vorher 60px */
  left: 0;
  width: 100%;
  z-index: 1000;
  padding: 5px 0;
  gap: 5px; /* Abstand zwischen Buttons */
  justify-content: center;
  align-items: center;
}

.settings-container button {
  padding: 0.5em 1.0em;
}

/*
.buy-container {
  background-color: var(--accent-header-bg-color);
  box-shadow: 0 0 5px 2px var(--box-shadow-color);
  width: 100%;
  z-index: 1000;
  position: fixed;
  bottom: 0px;
  left: 0;
  padding-top: 10px; 
  padding-bottom: 5px;
  justify-content: center;
  align-items: center;
}
*/

.input {
  width: 100%;
  box-sizing: border-box;
}

.popup-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  /* verhindert Klicks auf darunter liegende Elemente */
  pointer-events: auto;
}

.popup-content {
  background: var(--box-bg-color);
  padding: 1em 2em;
  border-radius: 0.5em;
  width: 100%;
  min-width: 250px;
  max-width: 300px;
  text-align: center;
  word-wrap: break-word;
  /* Klicks nur auf das Popup zulassen */
  pointer-events: auto;
  box-shadow: 0 4px 12px var(--box-shadow-color);
}

@media (max-width: 480px) {
  .popup-content {
    max-width: 260px;
  }
}

.card-grid {
  padding-top: 130px;
}

.mitglieder-anzeige {
  display: flex;
  justify-content: space-between;
  margin-block: 15px;
}

.button-delete-member {
  background-color: transparent;
  border: none;
  color: #dc3545;
  font-weight: bold;
  cursor: pointer;
  padding: 0 0.5em;
  font-size: 0.9rem;
  transition: color 0.3s ease;
}

.button-delete-member:hover {
  color: darkred;
}
</style>
