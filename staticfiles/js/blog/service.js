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


// TODO: Render the blog page using d3js
var render_blog = (blogs) => {
    console.log("rendering");
    console.log(blogs);

    allb = allb.concat(blogs);

    let area = d3.select("#blog-listing")
        .selectAll("div");

    let content = area.data(blogs, (b) => { return b.id })
        .enter()
        .append("div")
        .attr('class', 'col-12 col-xl-6')
        .attr('style','padding-bottom:20px;')
        .append('div')
        .attr('class', 'blog-content flex')

    content.append('figure')
        .append('a')
        .attr('href', '#')
        .append('img')
        .attr('style', 'object-fit: cover;height:300px')
        .attr('src', (d) => { return d.cover });


    let entry_content = content.append('div')
        .attr('class', 'entry-content flex flex-column justify-content-between align-items-start');

    let header = entry_content.append('header')
    header.append('h3')
        .append('a')
        .attr('href', (d) => { return '/blog/detail/' + d.id })
        .text((d) => { return d.title });
    header.append('div')
        .attr('class', 'posted-by')
        .text((d) => { return d.author })
    /*header.append('div')
        .attr('class', 'posted-by')
        .append('p')
        .text((d) => { return d.abstract })*/

    let footer = entry_content.append('footer')
        .attr('class', 'flex flex-wrap align-items-center');
    footer.append('div')
        .attr('class', 'posted-on')
        .text((d) => { return d.uploaded_at_formatted });
    footer.append('ul')
        .attr('class', 'flex flex-wrap align-items-center')
        .append('li')
        .append('a')
        .attr('href', (d) => { return '/blog/detail/' + d.id })
        .text("Portfolio");





}

var fetch = (init_fetch) => {
    console.log("fetching...", start, number);
    $('#load-more-blogs').prop('disabled', true);
    $.ajax({
        url: blog_fetch_url,
        method: 'POST',
        data: {
            start: start,
            number: init_fetch==true?number:increment,
        },

    }).done((data) => {
        if (data.status == 'success') {

            start += data.blogs.length;
            render_blog(data.blogs);
            $('#load-more-blogs').prop('disabled', false);
        } else {
            console.log(data);
            $('#load-more-blogs').prop('disabled', false);
        }
        
    })
}