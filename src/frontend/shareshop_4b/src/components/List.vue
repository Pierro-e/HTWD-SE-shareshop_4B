<template>
  <div class="liste">
    <div class="header">
      <button
        :disabled="showpopup_product || showpopup_list || showpopup_add_member"
        @click="$router.push('/listen')"
        class="button button-cancel back-button"
      >
        Zurück
      </button>

      <h2>{{ list_name }}</h2>

      <button
        :disabled="showpopup_product || showpopup_list || showpopup_add_member"
        @click="openProductPopup()"
        class="button button-add button-add-header"
      >
        Produkt hinzufügen
      </button>
    </div>

    <div class="settings-section">
      <div class="settings-container">
        <button
          :disabled="
            showpopup_product || showpopup_list || showpopup_add_member
          "
          @click="openListPopup()"
          class="button button-settings"
        >
          Listeninformationen
        </button>

        <button
          :disabled="
            showpopup_product || showpopup_list || showpopup_add_member
          "
          @click="einkauf_abschließen"
          class="button button-submit button-einkauf-tätigen"
        >
          Einkauf
        </button>
      </div>
    </div>

    <div v-if="showpopup_list" class="popup-overlay">
      <div class="popup-content">
        <h3>Listeninformationen</h3>
        <p>Name der Liste: {{ list_name }}</p>
        <p>Ersteller: {{ list_creator_name }}</p>
        <p><u>Mitglieder</u></p>
        <div
          v-for="mitglied in mitglieder"
          :key="mitglied.id"
          class="mitglieder-anzeige"
        >
          <p>{{ mitglied.name }}</p>
          <button
            @click="mitglied_entfernen(mitglied.id)"
            class="button button-delete-member"
          >
            Entfernen
          </button>
        </div>
        <button @click="showpopup_list = false" class="button button-cancel">
          Schließen
        </button>
        <button @click="mitglied_hinzufügen_popup()" class="button button-add">
          Mitglied hinzufügen
        </button>
      </div>
    </div>

    <div v-if="showpopup_product" class="popup-overlay">
      <div class="popup-content">
        <h3>Neues Produkt hinzufügen</h3>
        <input
          class="input"
          v-model="new_product"
          type="text"
          placeholder="Produktname"
          maxlength="30"
        />
        <div v-if="errorMessage" class="error">{{ errorMessage }}</div>
        <button @click="cancel_product_popup" class="button button-cancel">
          Abbrechen
        </button>
        <button @click="add_product" class="button button-add">
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
        <button @click="mitglied_hinzufügen" class="button button-add">
          Hinzufügen
        </button>
      </div>
    </div>

    <div class="produkte-grid">
      <div
        v-for="(produkt, index) in listenprodukte"
        :key="index"
        class="produkt-card"
      >
        <div class="produkt-header">
          <h3 class="produkt-name">
            {{ produkt.name || "Unbekanntes Produkt" }}
          </h3>
          <button
            @click="product_settings(produkt)"
            class="button button-product-settings"
          >
            ✏️
          </button>
        </div>

        <div class="produkt-info" v-if="produkt.produkt_menge">
          <div v-if="produkt.produkt_menge" >
            <strong>Menge:</strong> {{ produkt.produkt_menge }} {{ produkt.einheit_abk }}
          </div>
        </div>
        <div class="produkt-info" v-else>
          <span style="visibility: hidden">Platzhalter</span>
        </div>

        <div class="produkt-beschreibung" v-if="produkt.beschreibung">
          <p v-if="produkt.beschreibung">
            {{ produkt.beschreibung }}
          </p>
        </div>
        <div class="produkt-beschreibung" v-else>
          <p style="visibility: hidden">Platzhalter</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { inject } from "vue";

export default {
  name: "Liste",
  inject: ["user", "getUser"],
  props: ["list_id"],
  data() {
    return {
      list_name: "",
      list_creator_id: null,
      list_creator_name: "",
      errorMessage: "",
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

        for (const produkt of this.listenprodukte) {
          // Produktname holen
          try {
            const res1 = await axios.get(
              `http://141.56.137.83:8000/produkte/by-id/${produkt.produkt_id}`,
            );
            produkt.name = res1.data.name;
          } catch (innerError) {
            produkt.name = "[Fehler beim Laden]";
          }

          // Einheit holen
          try {
            const res2 = await axios.get(
              `http://141.56.137.83:8000/einheiten/${produkt.einheit_id}`,
            );
            produkt.einheit_abk = res2.data.abkürzung;
          } catch (innerError) {
            produkt.einheit_abk = "";
          }

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
    },

    openListPopup() {
      this.errorMessage = "";
      this.showpopup_list = true;
      this.showpopup_product = false;
      this.get_list_members(this.list_id);
    },

    openProductPopup() {
      this.errorMessage = "";
      this.showpopup_product = true;
      this.showpopup_list = false;
    },

    async add_product() {
      const list_id = this.list_id || this.$route.params.id;
      const user_id = this.user.id;

      this.errorMessage = "";

      if (this.new_product.trim() === "") {
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
              return;
            }
          }
        }
      }

      if (!list_id || !produkt_Id || !user_id) {
        console.log("Fehlende Liste-, Produkt- oder Nutzer-ID");
        return;
      }

      try {
        await axios.post(
          `http://141.56.137.83:8000/listen/${list_id}/produkte/${produkt_Id}/nutzer/${user_id}`,
        );
        this.showpopup_product = false;
        this.errorMessage = "";
        this.new_product = "";
      } catch (error) {
        if (error.response) {
          this.errorMessage =
            error.response.data.detail ||
            "Unbekannter Fehler beim Hinzufügen des Produkts zur Liste";
        }
      }
      this.get_products(list_id);
    },

    cancel_product_popup() {
      this.errorMessage = "";
      this.showpopup_product = false;
      this.new_product = "";
    },

    mitglied_hinzufügen_popup() {
      this.errorMessage = "";
      this.showpopup_list = false;
      this.showpopup_add_member = true;
    },

    async mitglied_entfernen(nutzer_id) {
      this.errorMessage = "";
      const listen_id = this.list_id || this.$route.params.id;
      console.log(`Entferne Mitglied ${nutzer_id} aus Liste ${listen_id}`);

      try {
        await axios.delete(
          `http://141.56.137.83:8000/listen/${listen_id}/mitglieder/${nutzer_id}`,
        );
        // Nach erfolgreichem Entfernen Mitgliederliste neu laden
        await this.get_list_members(listen_id);
      } catch (error) {
        if (
          error.response &&
          error.response.data &&
          error.response.data.detail
        ) {
          this.errorMessage = error.response.data.detail;
        } else {
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
      console.log(`Suche nach E-Mail: ${user_email}`);

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

    product_settings(produkt) {
      this.errorMessage = "";
      const list_id = this.list_id || this.$route.params.id;
      const product_id = produkt.produkt_id;
      const nutzer_id = produkt.hinzugefügt_von;

      this.$router.push(
        `/listen/${list_id}/produkte/${product_id}/nutzer/${nutzer_id}`,
      );
    },

    einkauf_abschließen() {
      const list_id = this.list_id || this.$route.params.id;

      this.$router.push(`/list/${list_id}/einkauf`);
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
.liste {
  padding-top: 50px;
}

/* Zurück-Button links */
.back-button {
  position: absolute;
  left: 20px;
  top: 25px;
}

/* Produkt hinzufügen Button rechts */
.button-add-header {
  position: absolute;
  right: 20px;
  top: 25px;
}

.button-einkauf-tätigen {
  position: relative;
  margin-top: 0px;
}

/* Settings-Container fixiert unter der Überschrift mittig */
.settings-container {
  position: fixed;
  top: 100px; /* vorher 60px */
  left: 0;
  width: 100%;
  z-index: 1000;
  padding: 5px 0;
  display: flex;
  flex-direction: column;
  gap: 10px; /* Abstand zwischen Buttons */
  justify-content: center;
  align-items: center;
}

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
  background: #2a2a2a;
  color: white;
  padding: 1em 2em;
  border-radius: 0.5em;
  width: 100%;
  min-width: 250px;
  max-width: 300px;
  text-align: center;
  /* Klicks nur auf das Popup zulassen */
  pointer-events: auto;
}

@media (max-width: 480px) {
  .popup-content {
    max-width: 260px;
  }
}

.mitglieder-anzeige {
  display: flex;
  justify-content: space-between;
}

.button-delete-member {
  background-color: transparent;
  border: none;
  color: red;
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
