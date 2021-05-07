<template>
<div>
  <div class="help-top">

  </div>

  <div class="accordian">
    
    <div class="accordian_item">
      <h2>
        <button class="accordian_question">
           Where do I find the building QR Codes?
        </button>
      </h2>

      <div class="accordian_collapse">
        <div class="accordian_content">
          You will find QR codes on select buildings 
          around the campus. You may scan them using the 
          “Scan QR” feature of this application.
        </div>
      </div>
    </div>

    <div class="accordian_item">
      <h2>
        <button class="accordian_question">
           How do I share my location?
        </button>
      </h2>

      <div class="accordian_collapse">
        <div class="accordian_content">
          Lorem ipsum dolor sit amet consectetur adipisicing elit. 
          Ipsa quidem animi eligendi quas rem voluptatem soluta adipisci natus veniam, 
          at dolores ut sed, nesciunt ab distinctio quo eum, autem nam!
        </div>
      </div>
    </div>

    <div class="accordian_item">
      <h2>
        <button class="accordian_question">
           Where do I enter my destination location?
        </button>
      </h2>

      <div class="accordian_collapse">
        <div class="accordian_content">
          Lorem ipsum dolor sit amet, consectetur adipisicing elit. Repudiandae, a? 
          Nostrum sit est quae cumque? Necessitatibus maxime reprehenderit quos
          perspiciatis excepturi, incidunt quam pariatur non optio delectus eligendi totam modi!
        </div>
      </div>
    </div>

    <div class="accordian_item">
      <h2>
        <button class="accordian_question">
           Lorem ipsum dolor sit amet consectetur adipisicing elit?
        </button>
      </h2>

      <div class="accordian_collapse">
        <div class="accordian_content">
         Lorem, ipsum dolor sit amet consectetur adipisicing elit. 
         Dicta cum odio ipsum modi quisquam minus fugit quas dignissimos 
         voluptatem, sit enim dolores! Nam possimus magnam aspernatur 
         consectetur, ut consequatur soluta.
        </div>
      </div>
    </div>

    <div class="accordian_item">
      <h2>
        <button class="accordian_question">
           Lorem ipsum dolor sit amet consectetur adipisicing elit. 
        </button>
      </h2>

      <div class="accordian_collapse">
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

}
</script>

<style>
  :root{
    --accordian-blue: rgb(44, 105, 198,0.47); 
  }

  h1,h2,h3{
    margin-top: 0;
  }

  .accordian_item{
    background: var(--accordian-blue);
    border-radius: 0.5rem;
  }
  .accordian_question{
    border: none;
    padding: 0rem;
    background: transparent;
    font-size: 1rem;
  }

  .accordian_content{
    font-size: 0.75rem;
    line-height: 1.4;
  }
</style>