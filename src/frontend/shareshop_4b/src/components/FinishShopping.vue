<template>
  <NumInput v-model:num="totalPrice" label="Gesamtpreis (€):" />
  <div v-if="errorMessage" class="error">{{ errorMessage }}</div>
  <button @click="finish" class="button button-submit">Fertig</button>
</template>

<script>
import NumInput from "./input/NumInput.vue";
import { inject } from "vue";
import axios from "axios";

export default {
  inject: ["user", "updateProducts", "products"],
  components: {
    NumInput,
  },
  data() {
    return { errorMessage: "", totalPrice: 0 };
  },
  methods: {
    async finish() {
      try {
        const list_id = this.$route.params.listenId;

        /* Eingabe kontrollieren */
        if (this.totalPrice < 0) {
          this.errorMessage = "Bitte geben Sie einen gültigen Gesamtpreis ein.";
          return;
        }

        /* Einkauf speichern */
        const response = await axios.post(
          `http://141.56.137.83:8000/create/einkaufsarchiv/list/${list_id}`,
          {
            eingekauft_von: this.user.id,
            gesamtpreis: this.totalPrice,
          },
        );
        const purchase_id = response.data.einkauf_id;

        /* Einkauf archivieren */
        const erledigteProdukte = this.products.filter((p) => p.erledigt);

        await Promise.all(
          erledigteProdukte.map((produkt) =>
            axios.post(
              `http://141.56.137.83:8000/create/eingekaufte_produkte/einkauf/${purchase_id}`,
              {
                produkt_id: produkt.produkt_id,
                produkt_menge: produkt.produkt_menge,
                einheit_id: produkt.einheit_id,
                hinzugefuegt_von: produkt.hinzugefügt_von,
                beschreibung: produkt.beschreibung,
              },
            ),
          ),
        );

        await Promise.all(
          erledigteProdukte.map((produkt) =>
            axios.post(
              `http://141.56.137.83:8000/bedarfsvorhersage_create/nutzer/${produkt.hinzugefügt_von}`,
              {
                produkt_id: produkt.produkt_id,
              },
            ),
          ),
        );

        /* eingekaufte Produkte entfernen */
        await Promise.all(
          erledigteProdukte.map((produkt) =>
            axios.delete(
              `http://141.56.137.83:8000/listen/${list_id}/produkte/${produkt.produkt_id}`,
              {
                data: {
                  hinzugefügt_von: produkt.hinzugefügt_von,
                },
              },
            ),
          ),
        );

        this.updateProducts();
        this.$parent.$emit("close");
      } catch (error) {
        console.log(error);
        if (
          error.response &&
          error.response.data &&
          error.response.data.detail
        ) {
          this.errorMessage = error.response.data.detail;
        } else {
          this.errorMessage = "Fehler beim Abschließen des Einkaufs.";
        }
      }
    },
  },
};
</script>
