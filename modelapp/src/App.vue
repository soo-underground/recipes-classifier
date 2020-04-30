<template>
  <v-app>
  <v-app-bar color="grey" dark app >
  <v-toolbar-title>Подбор тегов к рецептам</v-toolbar-title>
</v-app-bar>

    <v-content>
      <HelloWorld/>
    </v-content>
  </v-app>
</template>

<script>
import HelloWorld from './components/HelloWorld';

export default {
  name: 'App',

  components: {
    HelloWorld,
  },

  data: () => ({
    //
  }),
};
</script>
