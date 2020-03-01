<template>
<div id="htb-reco" :class="{ 'htb-open': open }">
    <div class="htb-button-open" @click="open = !open">
        <div class="inner">
            <i class="el-icon-d-arrow-left" v-show="!open"></i>
            <i class="el-icon-close" v-show="open"></i>
        </div>
    </div>
    <div class="htb-body-wrapper">
        <div class="htb-article" v-for="item in results" :key="item.uuid">
            <p><a :href="item.url" target="_blank">{{ item.title }}</a></p>
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
            open: false
        }
    },
    methods: {
        addStyle(css) {
            const style = document.createElement("style");
            style.type= "text/css";
            style.appendChild(document.createTextNode(css)); /* BUG: Does not work in IE8 or less */
            const inserted = document.body.appendChild(style);
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
            background: white;
        }
        `;

        this.addStyle(style)
        // console.log(this.$textData)
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

                data.forEach(element => {
                    
                    this.results.push(element)
                });
            })

            
    }
}
</script>