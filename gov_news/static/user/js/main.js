$(document).ready(function () {
  $(function () {
      // Sử dụng lớp hoặc id của carousel cụ thể ở đây (trong ví dụ này, là ".my-carousel" hoặc "#recipeCarousel")
      $('.my-carousel').carousel({
          interval: 10000
      })

      $('.my-carousel .carousel-item').each(function(){
          var minPerSlide = 4;
          var next = $(this).next();
          if (!next.length) {
              next = $(this).siblings(':first');
          }
          next.children(':first-child').clone().appendTo($(this));

          for (var i=0;i<minPerSlide;i++) {
              next=next.next();
              if (!next.length) {
                  next = $(this).siblings(':first');
              }

              next.children(':first-child').clone().appendTo($(this));
          }
      });

  });
});
