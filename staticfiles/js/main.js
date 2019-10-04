$(document).ready(function() {
    "use strict";
    // Empêcher la fermeture d'un clic à l'intérieur de la liste déroulante
    $(document).on('click', '.dropdown-menu', function(event) {
        event.stopPropagation();
    });

    // on fixe le menu lors le défilement de la page
    if ($(window).width() > 780) {
        $(window).scroll(function() {
            if ($(this).scrollTop() > 125) {
                $('.sticky').addClass('sticky-top');
            } else {
                $('.sticky').removeClass('sticky-top');
            }
        });
    }

    // Fancybox
    if ($('[data-fancybox="gallery"]').length > 0) {
        // statement
        $('[data-fancybox="gallery"]').fancybox();
    }

    // items slider
    //check if element exists
    if ($('.slick-slider').length > 0) {
        $('.slick-slider').slick({
            //dots: true,
            //speed: 300,
            //centerMode: true,
            //variableWidth: true,
            //adaptiveHeight: true,
            //autoplay: true,
            //autoplaySpeed: 2000,
            //slidesToScroll: 4,
            centerPadding: '40px',
            infinite: true,
            slidesToShow: 5,
            slidesToScroll: 4,
            responsive: [
                {
                    breakpoint: 992,
                    settings: {
                        arrows: true,
                        centerPadding: '20px',
                        slidesToShow: 3
                    }
                },

                {
                    breakpoint: 768,
                    settings: {
                        arrows: true,
                        centerPadding: '20px',
                        slidesToShow: 3
                    }
                },
                {
                    breakpoint: 600,
                    settings: {
                        slidesToShow: 2,
                        slidesToScroll: 2
                    }
                },
                {
                    breakpoint: 480,
                    settings: {
                        arrows: false,
                        //centerMode: true,
                        centerPadding: '50px',
                        slidesToShow: 1
                    }
                }
            ]
        });
    }

    if ($('.owl-init').length > 0) {
        // check if element exists
        $(".owl-init").each(function(){
            var myOwl = $(this);
            var data_items = myOwl.data('items');
            var data_nav = myOwl.data('nav');
            var data_dots = myOwl.data('dots');
            var data_margin = myOwl.data('margin');
            var data_custom_nav = myOwl.data('custom-nav');
            var id_owl = myOwl.attr('id');

            myOwl.owlCarousel({
                loop: true,
                margin: data_margin,
                nav: eval(data_nav),
                dots: eval(data_dots),
                autoplay: true,
                items: data_items,
                navText: ["<i class='fa fa-chevron-left'></i>", "<i class='fa fa-chevron-right'></i>"],
                items: 4,
                responsive: {
                    0: {
                        items: 1
                    },
                    600: {
                        items: data_items
                    },
                    1000: {
                        items: data_items
                    }
                }
            });

            // for custom navigation. See example page: example-sliders.html
            $('.'+data_custom_nav+'.owl-custom-next').click(function(){
                $('#'+id_owl).trigger('next.owl.carousel');
            });

            $('.'+data_custom_nav+'.owl-custom-prev').click(function(){
                $('#'+id_owl).trigger('prev.owl.carousel');
            });
        }); // each end.//
    }
});
