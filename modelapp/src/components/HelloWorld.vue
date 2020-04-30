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

<h1 v-if="predictedClass">Возможные теги: {{ predictedClass }}</h1>

<!-- END: IMPORTANT PART! -->
      </v-flex>


    </v-layout>


    <p> </p>
    <p> <b> Получить ответ напрямую от бекенда: </b> </p>
    <p> </p>
    <p> curl --location --request POST 'https://recipes-classifier-2.herokuapp.com/predict'  </p>
    <p>--header 'Content-Type: application/json'  </p>
    <p>--header 'Content-Type: text/plain'  </p>
    <p>--data-raw '{"input":"Рецепт борща"}'</p>
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
    axios({
      name: 'HelloWorld',
      method: 'post',
      url: 'https://recipes-classifier-2.herokuapp.com/predict',
      withCredentials: false,
      headers: {'Content-Type': 'application/json'},

      data: {
       input: this.sepalLength
      }
    }).then((response) => {
        this.predictedClass = response.data.response
      });
    },
    clear () {
      this.sepalLength = ''
    }
  }
}
</script>
