<template>
    <div class="dsahboard">
        <button @click="this.testReq()">test</button>
        {{ Response }}
        <h1>dsahboard</h1>
        <h2>category</h2>
        <table>
            <thead>
                <tr>
                    <td>id</td>
                    <td>name</td>
                    <td>description</td>
                    <td>created_at</td>
                    <td>created_by</td>
                    <td>updated_at</td>
                    <td>updated_by</td>
                    <td>delete</td>
                    <td>status</td>
                </tr>
            </thead>
            <tbody>
                <tr v-for="category in this.categories" :key="category.id">
                    <td>{{ category.id }}</td>
                    <td>{{ category.name }}</td>
                    <td>{{ category.description }}</td>
                    <td>{{ category.created_at }}</td>
                    <td>{{ category.created_by }}</td>
                    <td v-if='category.updated_at==null'>Not yet updated</td>
                    <td v-else>{{ category.updated_at }}</td>
                    <td v-if='category.updated_by==null'>Not yet updated</td>
                    <td v-else>{{ category.updated_by }}</td>
                    <td v-if="category.delete == false"><button @click="this.deleteCategory(category.id)">delete</button></td>
                    <td>{{ category.status }}</td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script>
import axios from 'axios'
    export default{
        data(){
            return{
                Response: "",
                token: null,
                categories: null
            }
        },
        beforeCreate(){
            if(localStorage.getItem('authToken') == null){
                this.$router.push({name: 'loginRoute'})
            }
            
        },
        created(){
            this.token = localStorage.getItem('authToken')
            if (this.token) {
                this.getCategory()
            }
        },
        methods:{
            testReq(){
                console.log(this.token);
                
                axios.get('http://localhost:5000/api/storeNew', 
                        {headers: {
                            'Authorization': `${this.token}`
                    }}
                )
                .then((response) => {
                    console.log("good response",response)
                    this.Response = response.data
                })
                .catch((error) => {
                    console.log("bad response",error)
                    this.Response = error.response.data
                })
            },
            async getCategory(){
                axios
                    .get('http://localhost:5000/api/category', {
                        headers: {
                            'Authorization': `${this.token}`
                        }
                    })
                    .then((response) => {
                        console.log(response.data);
                        if (response.status === 200) {
                            this.categories = response.data.data;
                        }
                    })
                    .catch((error) => {
                        console.log(error);
                    });
            },
            async deleteCategory(id){
                axios
                    .delete(`http://localhost:5000/api/category/${id}`, {
                        headers: {
                            'Authorization': `${this.token}`
                        }
                    })
                    .then((response) => {
                        if (response.status === 201) {
                            alert('Category deleted successfully');
                            this.getCategory();
                        }
                    })
                    .catch((error) => {
                        alert('Failed to delete category');
                    });
            }
        }
    }
</script>

<style>
    table, th, td {
    border: 1px solid black;
    border-collapse: collapse;
    }
</style>