<template>
  <div class="user-settings">
    <h2>Profil bearbeiten</h2>

    <form @submit.prevent="updateUser">
      <div>
        <label for="email">Neue E-Mail:</label>
        <input v-model="email" 
            type="email" 
            id="email" 
            required 
        />
      </div>

      <div>
        <label for="password">Neues Passwort:</label>
        <input v-model="password" 
            type="password" 
            id="password" 
            required />
      </div>

      <button class="button-submit" type="submit">Änderungen speichern</button>
    </form>

    <div v-if="message" class="success">{{ message }}</div>
    <div v-if="errorMessage" class="error">{{ errorMessage }}</div>
  </div>
</template>

<script>
export default {
  name: 'UserSettings',
  data() {
    return {
      email: '',
      password: '',
      message: '',
      errorMessage: ''
    };
  },
  methods: {
    async updateUser() {
      try {
        // Beispiel: Axios PUT request
        const response = await fetch('/api/user/update', {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            email: this.email,
            password: this.password
          })
        });

        if (!response.ok) throw new Error('Fehler beim Aktualisieren');

        this.message = 'Daten erfolgreich aktualisiert!';
        this.error = '';
      } catch (err) {
        this.error = err.message || 'Unbekannter Fehler';
        this.message = '';
      }
    }
  }
};
</script>

<style scoped>
.success {
  color: green;
}

.error {
  color: #ff4c4c;
  margin-top: 0.8rem;
  text-align: center;
  font-weight: 600;
}
</style>


