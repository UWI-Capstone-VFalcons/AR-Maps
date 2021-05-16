<template>
  <div id="servertest">
    <p>server</p>
    <div id="indicator" :class="indicatorClass"></div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'TestServer',
  data(){
    return{
      indicatorClass:[]
    }
  },
  methods: {
    getMessage() {
      const path = this.$host+'api/test';
      axios.get(path)
        .then((res) => {
          let msg = res.data.test;
          if(msg == "Its working"){
            this.indicatorClass.push("working");
          }
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
<style scoped>
#servertest{
  height: 1rem;
  width: auto;
  margin: 5px;
  margin-top: 1.5rem;
  position: absolute;
  top: 0;
  right: 0;
  z-index: 10;
  display: flex;
  flex-direction: row;
  align-items: center;
}
#indicator{
  height: 10px;
  width: 10px;
  border-radius: 5px;
  border: 1px solid white;
  background-color: red;
}

p{
  margin: 0;
  padding-right: 5px;
}

.working{
  background-color: #00ff00 !important;
}
@media (max-width: 480px) {
  #servertest{
    margin-top: .5rem;
  } 
}
</style>
