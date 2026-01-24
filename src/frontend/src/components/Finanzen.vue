<template>
  <AppHeader :title="user?.name + '\'s Finanzen'">
    <template #left>
        <button
          @click="$router.push('/listen')"
          class="button button-cancel back-button"
        >
          <font-awesome-icon icon='arrow-left'/>
        </button>
    </template>

    <template #right></template>
  </AppHeader>

  <div v-if="loadingActive" class="loading">Laden...</div>
  <div v-if="errorMessage" class="error">{{ errorMessage }}</div>

  <main v-if="!loadingActive && !errorMessage">
    <div class="card-list">

      <h3>Ich bekomme Geld von</h3>

      <ProductCard
        v-for="f in forderungen"
        :key="f.schuldner_id"
        :product="mapForderung(f)"
        :hideSettings="true"
      >
      <!-- Extra Slot: Löschen-Button -->
      <template #extra>
        <button
        class="button button-danger"
        @click="markAsReceived(f)"
        >
        Geld erhalten
        </button>
      </template>
      </ProductCard>

      <p v-if="!forderungen.length">Niemand schuldet dir Geld.</p>

      <h3>Ich schulde Geld an</h3>

      <ProductCard
        v-for="s in schulden"
        :key="s.empfaenger_id"
        :product="mapSchuld(s)"
        :hideSettings="true"
      />

      <p v-if="!schulden.length">Du schuldest niemandem Geld.</p>
    </div>
  </main>

  <BottomBar :highlight-btn="5" />
</template>

<script>
import AppHeader from "./AppHeader.vue"
import ProductCard from "./ProductCard.vue"
import BottomBar from "./BottomBar.vue"
import axios from "axios"
import { inject } from "vue"

/**
 * Zeigt an, wieviel Geld der Nutzer von anderen Nutzern bekommt oder ihnen noch schuldet.
 * <br>Empfänger: Personen, von denen der Nutzer Geld bekommt
 * <br>Schuldner: Personen, denen der Nutzer Geld schuldet
 */

export default {
  components: {
    AppHeader,
    ProductCard,
    BottomBar
  },
  data() {
    return {
      user: null,
      forderungen: [],
      schulden: [],
      errorMessage: "",
      loadingActive: true
    }
  },
  computed: {
    saldoProNutzer() {
      const saldo = {}

      // Geld, das ich bekomme
      this.forderungen.forEach(e => {
        if (!saldo[e.schuldner_name]) saldo[e.schuldner_name] = 0
        saldo[e.schuldner_name] += e.betrag
      })

      // Geld, das ich schulde
      this.schulden.forEach(e => {
        if (!saldo[e.empfaenger_name]) saldo[e.empfaenger_name] = 0
        saldo[e.empfaenger_name] -= e.betrag
      })

      return saldo
    }
  },
  async mounted() {
    const userRef = inject("user")

    if (!userRef || !userRef.value) {
      this.errorMessage = "Nutzer nicht verfügbar"
      this.loadingActive = false
      return
    }
   
    this.$watch(
      () => userRef.value.id,
      (newId) => {
        console.log("WATCH user.id:", newId)
      if (newId) {
        this.user = userRef.value
        this.loadFinanzen(newId)
      }
      },
      { immediate: true }
    )
  },
  methods: {
    /**
     * Mappt forderungen-Objekt, sodass es korrekt in ProductCard angezeigt wird.
     * @param {object} f Forderung
     */
    mapForderung(f) {
      return {
       produkt_name: f.schuldner_name,
       produkt_menge: Number(f.betrag).toFixed(2),
       einheit_abk: "€",
       beschreibung: ""
      }
    },
    /**
     * Mappt schulden-Objekt, sodass es korrekt in ProductCard angezeigt wird.
     * @param {object} s Schulden
     */
    mapSchuld(s) {
      return {
       produkt_name: s.empfaenger_name,
       produkt_menge: Number(s.betrag).toFixed(2),
       einheit_abk: "€",
       beschreibung: ""
       }
    },
    /**
     * Markiert eine Forderung als erhalten.
     * Nach Bestätigung wird die Forderung über API gelöscht und Seite aktualisiert.
     * @param {object} f Erhaltene Forderung
     */
    async markAsReceived(f) {
      if (!confirm(`Geld von ${f.schuldner_name} wirklich erhalten?`)) return

      try {
        await axios.delete(
        `http://141.56.137.83:8000/kostenaufteilung/empfaenger/${this.user.id}/schuldner/${f.schuldner_id}`
        )

        // lokal entfernen (UI sofort aktualisieren)
        const index = this.forderungen.findIndex(x => x.schuldner_id === f.schuldner_id)
        if (index !== -1) {
          this.forderungen.splice(index, 1)
        }

      } catch (error) {
        alert(error.response?.data?.detail || "Fehler beim Löschen der Kostenaufteilung")
      }
    },
    /**
     * Holt Finanzen (Empfänger und Schuldner des Nutzers) von API. 
     * Empfänger wird in forderungen-Objekt und Schuldner in schulden-Objekt gespeichert.
     * @param user_id {number} ID des Nutzers
     */
    async loadFinanzen(user_id) {
      try {
        const [empfaengerRes, schuldnerRes] = await Promise.all([
          axios.get(`http://141.56.137.83:8000/kostenaufteilung/empfaenger/${user_id}`),
          axios.get(`http://141.56.137.83:8000/kostenaufteilung/schuldner/${user_id}`)
        ])

        this.forderungen = empfaengerRes.data
        this.schulden = schuldnerRes.data
      } catch (error) {
        this.errorMessage = error.response?.data?.detail || "Fehler beim Laden der Finanzen"
      } finally {
        this.loadingActive = false
      }
    }
  }
};
</script>

<style scoped>
.card-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.error {
  width: 300px;
}
</style>
