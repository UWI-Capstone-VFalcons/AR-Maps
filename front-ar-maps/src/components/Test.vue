<template>
  <div class="container">
    <button type="button" class="btn btn-primary">{{ msg }}</button>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Test',
  data() {
    return {
      msg: '',
    };
  },
  methods: {
    getMessage() {
      const path = this.$host+'api/test';
      axios.get(path)
        .then((res) => {
          this.msg = res.data.test;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
  },
  created() {
    this.getMessage();
  },
};
</script>
