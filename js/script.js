(function($){
  // Search
  var $searchWrap = $('#search-form-wrap'),
    isSearchAnim = false,
    searchAnimDuration = 200;

  var startSearchAnim = function(){
    isSearchAnim = true;
  };

  var stopSearchAnim = function(callback){
    setTimeout(function(){
      isSearchAnim = false;
      callback && callback();
    }, searchAnimDuration);
  };

  $('.nav-search-btn').on('click', function(){
    if (isSearchAnim) return;

    startSearchAnim();
    $searchWrap.addClass('on');
    stopSearchAnim(function(){
      $('.search-form-input').focus();
    });
  });

  $('.search-form-input').on('blur', function(){
    startSearchAnim();
    $searchWrap.removeClass('on');
    stopSearchAnim();
  });

  // Share
  $('body').on('click', function(){
    $('.article-share-box.on').removeClass('on');
  }).on('click', '.article-share-link', function(e){
    e.stopPropagation();

    var $this = $(this),
      url = $this.attr('data-url'),
      encodedUrl = encodeURIComponent(url),
      id = 'article-share-box-' + $this.attr('data-id'),
      title = $this.attr('data-title'),
      offset = $this.offset();

    if ($(document.getElementById(id)).length){
      var box = $(document.getElementById(id));

      if (box.hasClass('on')){
        box.removeClass('on');
        return;
      }
    } else {
      var box = $('<div>').attr('id', id).addClass('article-share-box');
      $('<input>').addClass('article-share-input').val(url).appendTo(box);
      var links = $('<div>').addClass('article-share-links').appendTo(box);
      var services = [
        ['Twitter', 'twitter', 'https://twitter.com/intent/tweet?text=' + encodeURIComponent(title) + '&url=' + encodedUrl],
        ['Facebook', 'facebook', 'https://www.facebook.com/sharer.php?u=' + encodedUrl],
        ['Pinterest', 'pinterest', 'https://pinterest.com/pin/create/button/?url=' + encodedUrl],
        ['LinkedIn', 'linkedin', 'https://www.linkedin.com/shareArticle?mini=true&url=' + encodedUrl]
      ];
      services.forEach(function(service){
        var link = $('<a>').attr({
          href: service[2], target: '_blank', rel: 'noopener noreferrer', title: service[0]
        }).addClass('article-share-' + service[1]).appendTo(links);
        $('<span>').addClass('fa fa-' + service[1]).appendTo(link);
      });

      $('body').append(box);
    }

    $('.article-share-box.on').removeClass('on');

    box.css({
      top: offset.top + 25,
      left: offset.left
    }).addClass('on');
  }).on('click', '.article-share-box', function(e){
    e.stopPropagation();
  }).on('click', '.article-share-input', function(){
    $(this).select();
  }).on('click', '.article-share-box-link', function(e){
    e.preventDefault();
    e.stopPropagation();

    window.open(this.href, 'article-share-box-window-' + Date.now(), 'width=500,height=450');
  });

  // Caption
  $('.article-entry').each(function(i){
    $(this).find('img').each(function(){
      if ($(this).parent().hasClass('fancybox') || $(this).parent().is('a')) return;

      var alt = this.alt;

      if (alt) $(this).after($('<span>').addClass('caption').text(alt));

      $(this).wrap($('<a>').attr({
        href: this.src, 'data-fancybox': 'gallery', 'data-caption': alt
      }));
    });

    $(this).find('.fancybox').each(function(){
      $(this).attr('rel', 'article' + i);
    });
  });

  if ($.fancybox){
    $('.fancybox').fancybox();
  }

  // Mobile nav
  var $container = $('#container'),
    isMobileNavAnim = false,
    mobileNavAnimDuration = 200;

  var startMobileNavAnim = function(){
    isMobileNavAnim = true;
  };

  var stopMobileNavAnim = function(){
    setTimeout(function(){
      isMobileNavAnim = false;
    }, mobileNavAnimDuration);
  };

  $('#main-nav-toggle').on('click', function(){
    if (isMobileNavAnim) return;

    startMobileNavAnim();
    $container.toggleClass('mobile-nav-on');
    stopMobileNavAnim();
  });

  $('#wrap').on('click', function(){
    if (isMobileNavAnim || !$container.hasClass('mobile-nav-on')) return;

    $container.removeClass('mobile-nav-on');
  });
})(jQuery);
