$(document).ready(function () {
  const searchForm = document.getElementById("search-form");

  $('.cross').on('click', function () {
    $('#search-input').val('');
  });

    $('.magnify').on('click', function () {
      searchForm.requestSubmit(); //Fill out this field
  });

  $('#search-input').on('keypress', function (e) {
    if (e.key === 'Enter') {
      searchForm.requestSubmit();
    }
  });

  $('#search-form').on('submit', function (e) {
    $('.artist-container').empty();
    if (!$('#search-input')[0].checkValidity()) {
        return; 
    }

    e.preventDefault(); 

    const input = $('#search-input').val().trim();

    $('.loading1').show();
    $('.result-list').empty();
    $(`.no-results`).hide();


    setTimeout(() => {
      $('.loading1').hide();
        $.ajax({
          url: `/api/search?q=${input}`,
          method: 'GET',
          success: function (response) {
            //console.log(response);
            if (response._embedded.results && response._embedded.results.length > 0) {
              response._embedded.results.forEach((r) => {
                const artist_id = r._links.self.href.split('artists/')[1];
                //console.log(artist_id);
                const card = `
                  <div class="result-card" id="${artist_id}">
                    ${
                      r._links.thumbnail.href === '/assets/shared/missing_image.png' 
                      ? `<img src="${window.location.origin}/static/images/artsy_logo.svg" alt="${r.title}">` 
                      : `<img src="${r._links.thumbnail.href}" alt="${r.title}">`
                    }
                    <p>${r.title}</p>
                  </div>
                `;
                $('.result-list').show();
                $('.result-list').append(card);
              });
            } else {
              $(`.no-results`).show();
              $(`.result-list`).hide();
            }
          },
          error: function (err) {
            alert('Error: ' + err.responseJSON.error);
          },
        });
    }, 1000);
  });

  $('.artist-container').empty();


  $('.result-list').on('click', '.result-card', function () {
    $('.loading2').show();
    $('.artist-container').empty();
    const artist_id = $(this)[0].id;
    $('.result-card').removeClass('selected');
    setTimeout(() => {
      $.ajax({
        url: `/api/artist/${artist_id}`,
        method: 'GET',
        success: function (r) {
          $('.loading2').hide();
          $(`#${artist_id}`).addClass('selected');
          if (r) {
              const biography = r.biography;
              const birthday = r.birthday;
              const deathday = r.deathday;
              const nationality = r.nationality;
              const name = r.name;
              //console.log(artist_id);
              const artist = `    
                <div class="artist-info">
                  <h3>${name}</h3> 
                  <h3>(${birthday} – ${deathday})</h3>
                </div>
                <h4>${nationality}</h4>
                <p class="biography">${biography}</p>`;
                $('.artist-container').append(artist);
                $('.artist-container').show();
            }
        },
        error: function (err) {
          alert('Error: ' + err.responseJSON.error);
        },
      });
    }, 1000);
  });
});
