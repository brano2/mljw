<template>
<div>
    <table>
        <tr>
            <th>Word</th>
            <th>Sentiment</th>
            <th>Magnitude</th>
        </tr>
        <tr v-for="item in results" :key="item.id">
            <td>{{ item.content }}</td>
            <td>{{ item.salience }}</td>
            <td>{{ item.sentiment }}</td>
            <td>{{ item.magnitude }}</td>
        </tr>
    </table>
</div>
</template>
<script>
import axios from "axios"
export default {
    data() {
        return {
            results: []
        }
    },
    mounted() {
        // console.log(this.$textData)
        axios.post('https://us-central1-htb-2020-269718.cloudfunctions.net/function-1', { text: this.$textData })
            .then(({ data }) => {
                const parsed = JSON.parse(data)

                Object.keys(parsed.content).forEach(key => {
                    // if (this.results.length > 5) return;
                    this.results.push({
                        id: key,
                        content: parsed.content[key],
                        salience: parsed.salience[key],
                        sentiment: parsed.sentiment[key],
                        magnitude: parsed.magnitude[key]
                    })
                })

                this.results.sort(function(a, b) {
                    return b.magnitude - a.magnitude;
                });

                console.log(this.results)
            })

            
    }
}
</script>
<style>
body {
    position: relative;
}

#kek {
    background: #fff;
    position: fixed;
    top: 0px;
    left: 0px;
    width: 200px;
}
</style>