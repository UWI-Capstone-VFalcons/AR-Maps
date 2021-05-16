<template>
  <div id="main">
    <div id="help-top">
      <img class='help-svg' src="../assets/svg/searching.svg" alt="Home Search">
    </div>
   
    <div class="accordian">
    
      <div class="accordian_item">
        <button class="accordian_question">
            Where do I find the building QR Codes?
        </button>

        <div class="accordian_collapse open">
          <div class="accordian_content">
            You will find QR codes on select buildings 
            around the campus. You may scan them using the 
            “Scan QR” feature of this application.
          </div>
        </div>
      </div>

      <div class="accordian_item">
        <button class="accordian_question">
            How do I share my location?
        </button>
        

        <div class="accordian_collapse collapse open">
          <div class="accordian_content">
            Lorem ipsum dolor sit amet consectetur adipisicing elit. 
            Ipsa quidem animi eligendi quas rem voluptatem soluta adipisci natus veniam, 
            at dolores ut sed, nesciunt ab distinctio quo eum, autem nam!
          </div>
        </div>
      </div>

      <div class="accordian_item">
        <button class="accordian_question">
            Where do I enter my destination location?
        </button>
        

        <div class="accordian_collapse collapse open">
          <div class="accordian_content">
            Lorem ipsum dolor sit amet, consectetur adipisicing elit. Repudiandae, a? 
            Nostrum sit est quae cumque? Necessitatibus maxime reprehenderit quos
            perspiciatis excepturi, incidunt quam pariatur non optio delectus eligendi totam modi!
          </div>
        </div>
      </div>

      <div class="accordian_item">
        <button class="accordian_question">
            Lorem ipsum dolor sit amet consectetur adipisicing elit?
        </button>
        

        <div class="accordian_collapse collapse open">
          <div class="accordian_content">
            Lorem, ipsum dolor sit amet consectetur adipisicing elit. 
            Dicta cum odio ipsum modi quisquam minus fugit quas dignissimos 
            voluptatem, sit enim dolores! Nam possimus magnam aspernatur 
            consectetur, ut consequatur soluta.
          </div>
        </div>
      </div>

      <div class="accordian_item">
        <button class="accordian_question">
            Lorem ipsum dolor sit amet consectetur adipisicing elit. 
        </button>
        

        <div class="accordian_collapse collapse open">
          <div class="accordian_content">
            Lorem ipsum dolor, sit amet consectetur adipisicing elit.
            Vero incidunt aliquam vitae, asperiores veniam optio ipsam tempora ratione,
            illum aperiam repellendus aspernatur, dignissimos sequi iste nihil
            quam delectus voluptatem hic.
          </div>
        </div>
      </div>
    </div>  
  </div>     
</template>
<script>
export default {
  name:"Help_Section",
  mounted(){
    document.querySelectorAll('.accordian_question').forEach((item)=>{
    item.addEventListener('click',(event)=>{
        console.log("click!");

        if(!item.classList.contains('open')){
            console.log("adding collapsing class")
            item.nextElementSibling.classList = 'accordian_collapse collapsing';

            setTimeout(()=>{
                item.nextElementSibling.classList = 'accordian_collapse';
            },300);
        }else{
            item.nextElementSibling.classList = 'accordian_collapse collapsing';

            setTimeout(()=>{
                console.log("accordion now callapsed")
                item.nextElementSibling.classList = 'accordian_collapse open';
            },300);
        }
        item.classList.toggle("open");
        // item.nextElementSibling.classList.toggle("open")
        console.log(event);
      });
    });

  },  
}

</script>
<style scoped>
@media (max-width: 480px) {
  #main{
    flex-flow: column;
    flex-wrap: nowrap !important;
    justify-content: unset !important;
  }
  #help-top{
    width: 100%;
    height: auto;
    padding: 0.5rem 2rem;
  }

  #help-top img{
    width: 100% !important;
    height: auto !important;
  }
}

h1,h2,h3{   
    margin-top: 0;
}

#main{
  width: 100%;
  height: 100%;
  display:flex;
  flex-wrap: wrap;
  justify-content: center;
  padding: 1rem;
  overflow-y: auto;
  overflow-x: hidden;
}

#help-top{
  display:flex;
  align-items: center;
  justify-content: center;
}

/* .help-top-sub{
  display: flex;
  flex-direction: column;
  color: white;
  height: 5rem;
  padding: 0;
  margin: 0;
} */

#help-top h6{
  cursor: pointer;
  padding-top: 5px;
}

#help-top img{
  width: 35rem;
  height: 35rem;
}

.accordian{
    display: flex;
    flex-direction: column;
    flex: 1;
    justify-content: space-between;
}


.accordian_item{
    background: var(--accordian-blue);
    border-radius: 0.5rem;
    margin: .5rem;

    padding: 0.5rem;
   
}
.accordian_question{
    border: none;
    display: flex;
    justify-content: space-between;
    padding: 0.5rem;
    background: transparent;
    font-size: 1rem;
    width: 100%;
    text-align: left;
}

.accordian_question::after{
    content: " ";
    width: 0.625rem;
    height: 1rem;
    background-image: url("../assets/svg/drop-down.svg");
    background-repeat: no-repeat;
    background-size: contain;
    background-position: center center;
    display: flex;
    justify-content: space-between;
    transition: transform 300ms ease-in-out;
}

.accordian_question.open{
    font-weight: bold;
}

.accordian_question.open::after{
    transform: rotate(180deg);
}

.accordian_question:focus,
.accordian_question:focus-visible{
    border: none;
    outline: solid 1px var(--accordian-blue);
}

.accordian_content{
    font-size: 0.75rem;
    line-height: 1.4;
}

.accordian_collapse.open{
    display: none;
}

/* .accordian_collapse.collapse{
    display: none;
} */

.accordian_collapse.collapsing{
    height: 0rem;
    overflow:hidden;
    transition: height .35s ease-in;
}

</style>