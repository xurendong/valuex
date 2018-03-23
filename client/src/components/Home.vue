<template>
  <div>
    <p>Home page</p>
    <p>Random number: {{ randomNumber }}</p>
    <button @click="getRandom">new random</button>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data () {
    return {
      randomNumber: 0
    }
  },
  methods: {
    getRandomFromServer () {
      const path = `http://localhost:8080/random`
      axios.get(path)
      .then(response => {
        this.randomNumber = response.data.randomNumber
      })
      .catch(error => {
        console.log(error)
      })
    },
    getRandom () {
      this.getRandomFromServer()
    }
  },
  created () {
    this.getRandom()
  }
}
</script>
