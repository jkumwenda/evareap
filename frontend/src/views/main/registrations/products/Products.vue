<template>
    <div class="flex flex-col space-y-4 flex-1">
        <HeaderView :headerTitle="headerTitle"></HeaderView>
        <div class="flex flex-col space-y-4">
            <div class="flex justify-between items-center">
                <search-component @search="handleSearch"></search-component>
                <router-link :to="{ name: 'AddProduct' }" v-if="permissions.includes('ADD_PRODUCT')"
                    class="mt-2 px-4 py-2 text-catskill-white-100 bg-gradient-to-r from-catalina-blue-300 to-catalina-blue-500 hover:from-catalina-blue-400 hover:to-catalina-blue-600 rounded-xl">
                    Add Product</router-link>
            </div>
            <SpinnerComponent v-if="isLoading" />
            <div v-else class="rounded-2xl bg-catskill-white-100 shadow-sm p-4">
                <div class="flex flex-row bg-athens-gray-500 p-2 text-sm font-bold">
                    <div class="sm:w-1/12">Product ID</div>
                    <div class="sm:w-3/12">Product name</div>
                    <div class="sm:w-2/12">Generic name</div>
                    <div class="sm:w-3/12">Applicant</div>
                    <div class="sm:w-1/12">Date of Entry</div>
                    <div class="sm:w-1/12">Expiry Date</div>
                    <div class="sm:w-1/12">Status</div>
                    <div class="sm:w-1/12">Action</div>
                </div>
                <div class="flex flex-row p-2 text-sm items-center" v-for="(product, index) in products" :key="product.id"
                    :class="getRowClass(index)">
                    <div class="sm:w-1/12">PMRA/PL{{ product.product_id }}</div>
                    <div class="sm:w-3/12">{{ product.product_name }}</div>
                    <div class="sm:w-2/12">{{ product.generic_name.generic_name }}</div>
                    <div class="sm:w-3/12">{{ product.applicant.applicant }}</div>
                    <div class="sm:w-1/12">{{ formatDate(product.entry_date) }}</div>
                    <div class="sm:w-1/12">{{ formatDate(product.expiry_date) }}</div>
                    <div class="sm:w-1/12">Active</div>
                    <div class="flex space-x-2 sm:w-1/12">
                        <router-link v-if="permissions.includes('VIEW_PRODUCT')" class="p-1 bg-dodger-blue-50 rounded-full"
                            :to="{ name: 'Product', params: { id: product.id } }">
                            <EyeIcon class="w-5 h-5 text-catalina-blue-300"></EyeIcon>
                        </router-link>
                        <router-link v-if="permissions.includes('UPDATE_PRODUCT')" class="p-1 bg-spray-200 rounded-full"
                            :to="{ name: 'EditProduct', params: { id: product.id } }">
                            <PencilSquareIcon class=" w-5 h-5 text-spray-700">
                            </PencilSquareIcon>
                        </router-link>
                        <div v-if="permissions.includes('DELETE_PRODUCT')" class="p-1 bg-flamingo-100 rounded-full">
                            <TrashIcon class="w-5 h-5 text-flamingo-500" @click="showDeleteConfirmation(product.id)">
                            </TrashIcon>
                        </div>
                    </div>
                </div>
                <pagination-component :currentPage="currentPage" :totalPages="totalPages" @page-change="handlePageChange">
                </pagination-component>
            </div>
        </div>
        <delete-confirmation-modal :show="showDeleteModal" @confirmed="deleteProduct(deleteProductId)"
            @canceled="cancelDelete"></delete-confirmation-modal>
    </div>
</template>

<script>
import HeaderView from '@/includes/Header.vue'
import { EyeIcon, PencilSquareIcon, TrashIcon } from '@heroicons/vue/24/solid'
import PaginationComponent from '@/components/PaginationComponent.vue'
import SearchComponent from '@/components/SearchComponent.vue'
import { fetchData, deleteItem } from "@/services/apiService";
import SpinnerComponent from "@/components/Spinner.vue";
import DeleteConfirmationModal from "@/components/DeleteConfirmationModal.vue";
import { useAuthStore } from "@/store/authStore";

export default {
    name: 'ProductsView',
    components: {
        EyeIcon, PencilSquareIcon, TrashIcon, PaginationComponent, SearchComponent, HeaderView, SpinnerComponent, DeleteConfirmationModal
    },
    data() {
        return {
            headerTitle: "Medicine Products",
            products: {},
            isLoading: true,
            showDeleteModal: false,
            deletePersonnelId: null,
            currentPage: 1,
            totalPages: "",
            pageSize: process.env.VUE_APP_PAGE_SIZE,
            searchPhrase: ""
        };
    },
    mounted() {
        this.getProducts();
    },
    setup() {
        const authStore = useAuthStore()
        const permissions = authStore.permissions
        return { permissions }
    },
    methods: {
        async getProducts() {
            try {
                const response = await fetchData("products", this.currentPage, this.pageSize, this.searchPhrase);
                this.products = response.data;
                this.totalPages = response.pages;
                this.isLoading = false;
            } catch (error) {
                console.error("Error fetching products:", error);
                this.isLoading = false;
            }
        },
        async handleSearch(searchQuery) {
            this.searchPhrase = searchQuery
            this.getProducts();
        },
        async handlePageChange(newPage) {
            this.currentPage = newPage;
            this.getProducts();
        },
        async deleteProduct(id) {
            this.isLoading = true;
            try {
                await deleteItem("products", id);
                const index = this.products.findIndex((product) => product.id === id);
                if (index !== -1) {
                    this.products.splice(index, 1);
                }
                this.showDeleteModal = false;
                this.isLoading = false;
            } catch (error) {
                console.error("Error fetching products:", error);
                this.isLoading = false;
                this.showDeleteModal = false;
            }
        },
        showDeleteConfirmation(id) {
            this.deleteProductId = id;
            this.showDeleteModal = true;
        },
        cancelDelete() {
            this.showDeleteModal = false;
        },
        getRowClass(index) {
            return index % 2 === 0 ? 'bg-athens-gray-400' : 'bg-athens-gray-100';
        },
        formatDate(dateString) {
            const date = new Date(dateString);
            const formattedDate = date.toLocaleString("en-UK", {
                day: "2-digit",
                month: "2-digit",
                year: "numeric",
            });
            return formattedDate;
        },
    }
}
</script>