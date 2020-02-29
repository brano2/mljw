import './index.styl'
import Vue from 'vue'
import App from "../App.vue"

const allowed_sites = [
    {
        name: 'www.thesun.co.uk',
        article_selector: '.article__content',
        content_selector: '.article__content > p'
    },
    {
        name: 'www.theguardian.com',
        article_selector: '#article',
        content_selector: '#article .content__article-body p'
    },
    {
        name: 'www.bbc.co.uk',
        article_selector: '.story-body',
        content_selector: '.story-body__inner > p'
    },
    {
        name: 'www.independent.co.uk',
        article_selector: '.body-content',
        content_selector: '.body-content > p'
    },
    {
        name: 'www.ft.com',
        article_selector: '.article__content-body',
        content_selector: '.article__content-body > p'
    },
    {
        name: 'www.politico.eu',
        article_selector: '.story-text',
        content_selector: '.story-text > p'
    },
    {
        name: 'blogs.lse.ac.uk',
        article_selector: '.post-content',
        content_selector: '.pf-content > p'
    },
    {
        name: '',
        article_selector: '',
        content_selector: ''
    },
    {
        name: '',
        article_selector: '',
        content_selector: ''
    },
    {
        name: '',
        article_selector: '',
        content_selector: ''
    }
]

 

function $select(selector) {
    return Array.prototype.slice.call(document.querySelectorAll(selector))
}

function check_site(url) {
    let text = ""
    allowed_sites.forEach(site => {
        if (site.name === url) {
            if ($select(site.article_selector)) {
                const textNodes = $select(site.content_selector)
                textNodes.forEach(textNode => {
                    text += `\n${textNode.textContent}`
                })
            }
        }
    })
    return text
}

const url = window.location.hostname
const text = check_site(url)
if (text !== "") {
    console.log('site allowed')
    const check = $select('#kek')
    if (check.length > 0) {
        check.forEeach(el => {
            el.parentNode.removeChild(el);
        })
    }

    const elem = document.createElement('div');
    elem.id = "kek"
    document.body.appendChild(elem);

    Vue.prototype.$textData = text

    var app = new Vue({
        render: h => h(App)
    }).$mount('#kek')
} else {
    console.log("site not allowed")
}