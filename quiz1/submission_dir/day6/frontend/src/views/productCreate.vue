<template>
    <div class="createProduct">
        <h1>Add a new product to a category</h1>
            <form @submit.prevent="this.addProduct()">
                <label for="name">name: </label>
                    <input type="text" name="name" id="" v-model="this.name" required>
                <label for="description">description: </label>
                    <input type="text" name="description" id="" v-model="this.description" required>
                <label for="price">price: </label>
                    <input type="number" name="price" id="" v-model="this.price" required>
                <label for="stock">stock: </label>
                    <input type="number" name="stock" id="" v-model="this.stock" required>
                <label for="category">category: </label>
                    <select name="category" v-model="this.category_id" required>
                        <option  v-for="category in this.categories" :key="category.id" :value="category.id"><div v-if="category.status==true">{{ category.name }}</div></option>
                    </select>
                <button type="submit">Add</button>
            </form>
            
    </div>
</template>

<script>
import axios from 'axios';
export default {
    name: 'categoryCreate',
    data() {
        return {
            name: '',
            description: '',
            token: '',
            price: null,
            stock: null,
            category_id: null,
            categories: null
        }
    },
    beforeCreate() {
        // this.token = localStorage.getItem('authToken');
        if (!localStorage.getItem('authToken')) {
            this.$router.push({name: 'loginRoute'});
        }
        if (this.token && localStorage.getItem('role') !== 'admin') {
            this.$router.push({name: 'homeRoute'});
        }
    },
    created() {
        this.token = localStorage.getItem('authToken');
        if(this.token){
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
        }
    },
    methods: {
        addProduct() {
            if(this.name == '' || this.description == '' || this.price == null || this.stock == null || this.category_id == null){
                alert('All fields are required');
                return;
            }
            // if(this.category_id from this.categories == null){
            //     alert('Category does not exist');
            //     return;
            // }
           axios
                .post('http://localhost:5000/api/product', {
                    name: this.name,
                    description: this.description,
                    price: this.price,
                    stock: this.stock,
                    category_id: this.category_id
                }, {
                    headers: {
                        'Authorization': `${this.token}`
                    }
                })
                .then((response) => {
                    if (response.status === 201) {
                        alert('Product added successfully');
                        this.$router.push({name: 'homeRoute'});
                    }
                })
                .catch((error) => {
                    alert('Failed to add category');
                });
        }
    }
}
</script>