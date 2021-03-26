//
//                       _oo0oo_
//                      o8888888o
//                      88" . "88
//                      (| -_- |)
//                      0\  =  /0
//                    ___/`---'\___
//                  .' \\|     |// '.
//                 / \\|||  :  |||// \
//                / _||||| -:- |||||- \
//               |   | \\\  -  /// |   |
//               | \_|  ''\---/''  |_/ |
//               \  .-\__  '-'  ___/-. /
//             ___'. .'  /--.--\  `. .'___
//          ."" '<  `.___\_<|>_/___.' >' "".
//         | | :  `- \`.;`\ _ /`;.`/ - ` : | |
//         \  \ `_.   \_ __\ /__ _/   .-` /  /
//     =====`-.____`.___ \_____/___.-`___.-'=====
//                       `=---='
//
//
//     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//
//               佛祖保佑         永无BUG
//
//
//TODO: Select container to render

/**
 * 
 */

const TAG_STYLES = ["btn btn-primary tag",
"btn btn-secondary tag ",
"btn btn-success tag ",
"btn btn-danger tag ",
"btn btn-warning tag ",
"btn btn-info tag ",
"btn btn-light tag ",
"btn btn-dark tag "]

const UPLOAD_PLACEHOLDER = {
    "type":"placeholder",
    "file":"plus sign url",
    

}

let get_orientation_from_exif = (exif) => {
    let res;
    switch (exif[274]) {
        case 8:
            res = 'rotate270';
            break;
        default:
            res = '';
    }
    return res; 
}

let get_orientation = (photo) => {
    console.log(photo.exif);
    let exif = JSON.parse(photo.exif.replace(/&quot;/g, '"'));
    try{
        return get_orientation_from_exif(exif);

    } catch(e) {
        return '';
    }
    
}

let render_gallery = (photos) => {
    
    allp = allp.concat(photos);

    let selected = d3.select('#gallery_body')
        .selectAll('div')

    let content = selected
        .data(allp, (d) => { return d.id })
        .enter()
        .append('div')
        .attr('class', 'col-12 col-md-6 col-lg-4')
        .attr('style', 'padding-top:50;padding-bottom:0;padding-left:20;padding-left:20')
        .append('div')
        .attr('class', 'portfolio-content')



    content.append('figure')
        .append('img')
        .attr('class', get_orientation)
        .attr('src', (p) => { return p.thumbnail_url })
        .attr('style', 'object-fit: cover;height:300px');


    let ptext = content.append('div')
        .attr('class', 'entry-content flex flex-column align-items-center justify-content-center');

    ptext.append('h3')
        .append('a')
        .attr('href', '#')
        .text((p) => { return p.title })

    ptext.append('ul')
        .attr('class', 'flex flex-wrap justify-content-center')
        .append('li')
        .append('a')
        .attr('href', (p) => { return '/gallery/detail/' + p.id + '/'; })
        .text('story');

    selected
        .exit()
        .remove();


    console.log(allp, content);

}

var fetch = (init_fetch) => {
    $('#load-more').attr('disabled', true);
    $.ajax({
        url: fetch_url,
        method: "POST",
        data: {
            'start': start,
            'number': init_fetch==true?number:increment,
        }
    }).done(
        (data) => {
            $('#load-more').prop('disabled', true)
            start += data.photos.length;
            render_gallery(data.photos)
            $('#load-more').prop('disabled', false)
        }
    );

}

var get_tag = () => {
    var res_array = [];
    d3.select(".tag-display").selectAll(".tag").each((d,i)=>{res_array.push(d)});
    return res_array;

}

var add_tag = (tagname) => {

    let random_index = Math.floor((Math.random() * TAG_STYLES.length));
    let tag_array = get_tag();
    let text_position = $("#tag-add-input").offset();
    console.log(text_position);
    if (tag_array.indexOf(tagname.toLowerCase()) < 0) {
        tag_array.push(tagname.toLowerCase())
    }
    let update = d3.select(".tag-display").selectAll(".tag")
    .data(tag_array,(d) => {return d});

    update.enter()
    .append("button")
    .attr("type","button")
    .attr("class",TAG_STYLES[random_index])
    .text(tagname)

    .style("opacity",0)
    .style("left",'40px')
    .transition().duration(400)
    .style("opacity",1)
    .style("position","relative")
    .style("left",'0px')
    .style("top",'0px')
    
    
    ;

    console.log(text_position['left']+'px')



    update.exit().remove();
    

}

var remove_tag = (tagname)=>{
    let tag_array = get_tag().filter(v => v != tagname);
    console.log(tag_array)
    let update = d3.select(".tag-display").selectAll(".tag")
    .data(tag_array,(d)=>{return d}).exit();

    update
    .style("opacity",1)
    .transition()
    .duration(300)
    .style("opacity",0)
    .remove();

    



}


var extract_form = () => {
    let title = $("#title").val();
    let author = $("#author").val();
    let password = $("#password").val();
    let summary = $("#summary").val();
    let tags = get_tag();
    let file = $("#inputGroupFile02").prop("files")[0];

    if (tags != null && tags != undefined) {
        tags = tags.toString();
    }
    let data = {
        "title":title,
        "author":author,
        "password":password,
        "summary":summary,
        "tags":tags,
        "file":file
    }

    let form_data = new FormData();
    for (key in data) {
        form_data.append(key,data[key])
    }
    return form_data;
}

var upload = (data) => {
    let request = new XMLHttpRequest();
    request.open('POST', photo_upload_url);
    csrf = Cookies.get('csrftoken');
    // https://github.com/js-cookie/js-cookie/
     request.setRequestHeader("X-CSRFToken",csrf);
    request.send(data);
}