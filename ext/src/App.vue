<template>
<div id="htb-reco" :class="{ 'htb-open': open }">
    <div class="htb-button-open" @click="openModal()">
        <div class="inner">
            <i class="el-icon-d-arrow-left" v-if="!loading" v-show="!open"></i>
            <i class="el-icon-close" v-if="!loading" v-show="open"></i>
            <i class="el-icon-loading" v-if="loading"></i>
        </div>
    </div>
    <div class="htb-body-wrapper">
        <div class="htb-body-inner-wrapper">
            <div>
                <p class="small" style="font-size: 12px; margin-bottom: 10px;">{{ getText }}</p>
            </div>
            <div class="htb-article" v-for="item in results" :key="item.uuid">
                <a :href="item.url" target="_blank">
                    <img :src="item.thread.main_image">
                    <p>{{ item.title }}</p>
                </a>
            </div>
        </div>
    </div>
</div>
</template>
<script>
import axios from "axios"
export default {
    data() {
        return {
            results: [],
            stats: [],
            open: false,
            loading: false
        }
    },
    methods: {
        addStyle(css) {
            const style = document.createElement("style");
            style.type= "text/css";
            style.appendChild(document.createTextNode(css)); /* BUG: Does not work in IE8 or less */
            const inserted = document.body.appendChild(style);
        },
        openModal() {
            if (this.loading) return
            this.open = !this.open
        }
    },
    computed: {
        getText() {
            if (this.stats.length == 0) return ''

            if (this.stats[0].orig_sentiment < this.stats[0].recommendation_sentiment) {
                return `Here is an article which likes ${this.stats[0].keyword} better:`
            } else {
                return `Here is an article which doesn't like ${this.stats[0].keyword} as much:`
            }
        }
    },
    mounted() {
        const style = `
        body: {
            position: relative;
        }

        #htb-reco {
            position: fixed;
            top: 0px;
            right: -350px;
            width: 400px;
            z-index: 999999;
            display: flex;
            transition: right 0.4s ease-in-out;
        }

        #htb-reco.htb-open {
            right: 0px;
        }

        #htb-reco .htb-button-open {
            width: 50px;
            height: 50px;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        #htb-reco .htb-button-open .inner {
            width: 30px;
            height: 30px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: white;
            border-radius: 100px;
            border: 1px solid #f2f2f2;
            box-shadow: 0 1px 2px black;
        }

        #htb-reco .htb-body-wrapper {
            width: 350px;
            padding: 5px;
        }

         #htb-reco .htb-body-wrapper .htb-body-inner-wrapper {
            width: 340px;
            border-radius: 5px;
            background: #fff;
            border: 1px solid #f2f2f2;
            box-shadow: 0 1px 2px black;
            padding: 10px;
        }

        #htb-reco .htb-body-wrapper .htb-body-inner-wrapper img {
            border-radius: 5px;
            width: 100%;
        }

        #htb-reco .htb-body-wrapper .htb-body-inner-wrapper p {
            font-size: 18px;
            font-weight: bold;
        }

        #htb-reco .htb-body-wrapper .htb-body-inner-wrapper a {
            text-decoration: none;
        }
        `;

        this.addStyle(style)
        // console.log(this.$textData)
        this.loading = true;
        axios.post('http://127.0.0.1:5000/analyze_text', { text: this.$textData })
            .then(({ data }) => {
                // const parsed = JSON.parse(data)
                console.log('data', data)
                // Object.keys(parsed.content).forEach(key => {
                //     // if (this.results.length > 5) return;
                //     this.results.push({
                //         id: key,
                //         content: parsed.content[key],
                //         salience: parsed.salience[key],
                //         sentiment: parsed.sentiment[key],
                //         magnitude: parsed.magnitude[key]
                //     })
                // })

                // this.results.sort(function(a, b) {
                //     return b.magnitude - a.magnitude;
                // });

                // console.log(this.results)
                this.stats.push(data[0])
                this.results.push(data[1])
                this.loading = false
                this.open = true
            })

            
    }
}
</script>