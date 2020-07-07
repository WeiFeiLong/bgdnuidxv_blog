result = {{ result|safe }};
for (let i=0; i<result.length; i++){
    $('.home').append('<div class="col-xs-4 col-sm-3 col-md-2 col-lg-2"><div class="menu"><a href="https://'
        +result[i][3]+
        '" target="_blank"><img src="/media/'
        +result[i][4]+
        '" class="img-responsive" alt="Responsive image"></a><p>'
        +result[i][2]+
        '</p></div></div>'
    )
}