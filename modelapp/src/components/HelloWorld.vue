<template>
  <v-container>
    <v-layout
      text-xs-center
      wrap
    >
      <v-flex>
        <!-- IMPORTANT PART! -->

        <form>
          <v-textarea
            v-model="sepalLength"
            label="Введите рецепт"
            required
          ></v-textarea>




<v-btn @click="submit">Подобрать теги</v-btn>
          <v-btn @click="clear">Очистить</v-btn>
        </form>

<br/>
        <br/>

<h1 v-if="predictedClass">Predicted Class is: {{ predictedClass }}</h1>

<!-- END: IMPORTANT PART! -->
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
  import axios from 'axios'

  export default {
    name: 'HelloWorld',
    data: () => ({
      sepalLength: '',
      predictedClass : ''
    }),
    methods: {
    submit () {
      axios.get('https://recipes-classifier-2.herokuapp.com/predict',

      {
        input: this.sepalLength,
      })
      .then((response) => {
        this.predictedClass = response.data.class
      })
    },
    clear () {
      this.sepalLength = ''
      this.sepalWidth = ''
      this.petalLength = ''
      this.petalWidth = ''
    }
  }
}
</script>
