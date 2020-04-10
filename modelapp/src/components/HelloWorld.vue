<template>
  <v-container>
    <v-layout
      text-xs-center
      wrap
    >
      <v-flex>
        <!-- IMPORTANT PART! -->

<form>
          <v-text-field
            v-model="sepalLength"
            label="Sepal Length"
            required
          ></v-text-field>
          <v-text-field
            v-model="sepalWidth"
            label="Sepal Width"
            required
          ></v-text-field>
          <v-text-field
            v-model="petalLength"
            label="Petal Length"
            required
          ></v-text-field>
          <v-text-field
            v-model="petalWidth"
            label="Petal Width"
            required
          ></v-text-field><v-btn @click="submit">submit</v-btn>
          <v-btn @click="clear">clear</v-btn>
        </form>

        <br/>
                <br/>

<h1 v-if="predictedClass">Predicted Class is: {{ predictedClass }}
</h1>

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
          sepalWidth: '',
          petalLength: '',
          petalWidth: '',
          predictedClass : ''
        }),
        methods: {
        submit () {
          axios.post('http://127.0.0.1:5000/predict', {
            sepal_length: this.sepalLength,
            sepal_width: this.sepalWidth,
            petal_length: this.petalLength,
            petal_width: this.petalWidth
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
