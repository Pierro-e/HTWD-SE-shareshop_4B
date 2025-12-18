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

      <!-- Forderungen -->
      <div class="card">
        <h3>Ich bekomme Geld von</h3>
        <ul v-if="forderungen.length">
          <li v-for="f in forderungen" :key="f.schuldner_id">
            <strong>{{ f.schuldner_name }}</strong>:
            {{  Number(f.betrag).toFixed(2) }} €
          </li>
        </ul>
        <p v-else>Niemand schuldet dir Geld.</p>
      </div>

      <!-- Schulden -->
      <div class="card">
        <h3>Ich schulde Geld an</h3>
        <ul v-if="schulden.length">
          <li v-for="s in schulden" :key="s.empfaenger_id">
            <strong>{{ s.empfaenger_name }}</strong>:
            {{  Number(s.betrag).toFixed(2) }} €
          </li>
        </ul>
        <p v-else>Du schuldest niemandem Geld.</p>
      </div>

    </div>
  </main>

  <BottomBar :highlight-btn="1" />
</template>

<script>
import AppHeader from "./AppHeader.vue"
import BottomBar from "./BottomBar.vue"
import axios from "axios"
import { inject } from "vue"

export default {
  components: {
    AppHeader,
    BottomBar
  },
  data() {
   // const userRef = inject("user")
   // console.log("inject user:", userRef)
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
    console.log("userRef initial:", userRef.value)
    // Reaktiv auf User-ID warten
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
    //this.user = userRef.value
    //const user_id = this.user.id

        async loadFinanzen(user_id) {
            try {
            const [empfaengerRes, schuldnerRes] = await Promise.all([
                axios.get(`http://141.56.137.83:8000/kostenaufteilung/empfaenger/${user_id}`),
                axios.get(`http://141.56.137.83:8000/kostenaufteilung/schuldner/${user_id}`)
            ])

            this.forderungen = empfaengerRes.data
            this.schulden = schuldnerRes.data
            } catch (error) {
            this.errorMessage =
                error.response?.data?.detail || "Fehler beim Laden der Finanzen"
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

.card {
  background: #fff;
  padding: 1rem;
  border-radius: 8px;
}

.positiv {
  color: green;
}

.negativ {
  color: red;
}

.error {
  width: 300px;
}
</style>
