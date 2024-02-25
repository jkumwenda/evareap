<template>
    <div class="flex flex-col space-y-4 flex-1">
        <HeaderView :headerTitle="headerTitle"></HeaderView>
        <div class="flex flex-col space-y-4">
            <div class="flex justify-between items-center">
                <search-component @search="handleSearch"></search-component>
                <router-link :to="{ name: 'AddAdministrationRoute' }" v-if="permissions.includes('ADD_PRODUCT_CATEGORY')"
                    class="mt-2 px-4 py-2 text-catskill-white-100 bg-gradient-to-r from-catalina-blue-300 to-catalina-blue-500 hover:from-catalina-blue-400 hover:to-catalina-blue-600 rounded-xl">
                    Add Administration route</router-link>
            </div>
            <SpinnerComponent v-if="isLoading" />
            <div v-else class="rounded-2xl bg-catskill-white-100 shadow-sm p-4">
                <div class="flex flex-row bg-athens-gray-500 p-2 text-sm font-bold">
                    <div class="sm:w-4/12">Administration route</div>
                    <div class="sm:w-7/12">Description</div>
                    <div class="sm:w-1/12">Action</div>
                </div>
                <div class="flex flex-row p-2 text-sm items-center"
                    v-for="(administration_route, index) in administration_routes" :key="administration_route.id"
                    :class="getRowClass(index)">
                    <div class="sm:w-4/12">{{ administration_route.administration_route }}</div>
                    <div class="sm:w-7/12">{{ administration_route.description }}</div>
                    <div class="flex space-x-2 sm:w-1/12">
                        <router-link v-if="permissions.includes('UPDATE_PRODUCT_CATEGORY')"
                            class="p-1 bg-spray-200 rounded-full"
                            :to="{ name: 'EditAdministrationRoute', params: { id: administration_route.id } }">
                            <PencilSquareIcon class=" w-5 h-5 text-spray-700">
                            </PencilSquareIcon>
                        </router-link>
                        <div v-if="permissions.includes('DELETE_PRODUCT_CATEGORY')"
                            class="p-1 bg-flamingo-100 rounded-full">
                            <TrashIcon class="w-5 h-5 text-flamingo-500"
                                @click="showDeleteConfirmation(administration_route.id)">
                            </TrashIcon>
                        </div>
                    </div>
                </div>
                <pagination-component :currentPage="currentPage" :totalPages="totalPages" @page-change="handlePageChange">
                </pagination-component>
            </div>
        </div>
        <delete-confirmation-modal :show="showDeleteModal"
            @confirmed="deleteAdministrationRoute(deleteAdministrationRouteId)"
            @canceled="cancelDelete"></delete-confirmation-modal>
    </div>
</template>

<script>
import HeaderView from '@/includes/Header.vue'
import { PencilSquareIcon, TrashIcon } from '@heroicons/vue/24/solid'
import PaginationComponent from '@/components/PaginationComponent.vue'
import SearchComponent from '@/components/SearchComponent.vue'

import { fetchData, deleteItem } from "@/services/apiService";
import SpinnerComponent from "@/components/Spinner.vue";
import DeleteConfirmationModal from "@/components/DeleteConfirmationModal.vue";
import { useAuthStore } from "@/store/authStore";

export default {
    name: 'AdministrationRoutesView',
    components: {
        PencilSquareIcon, TrashIcon, PaginationComponent, SearchComponent, HeaderView, SpinnerComponent, DeleteConfirmationModal
    },
    data() {
        return {
            headerTitle: "Administration Route",
            administration_routes: {},
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
        this.getAdministrationRoutes();
    },
    setup() {
        const authStore = useAuthStore()
        const permissions = authStore.permissions
        return { permissions }
    },
    methods: {
        async getAdministrationRoutes() {
            try {
                const response = await fetchData("administration_routes", this.currentPage, this.pageSize, this.searchPhrase);
                this.administration_routes = response.data;
                this.totalPages = response.pages;
                this.isLoading = false;
            } catch (error) {
                console.error("Error fetching administration routes:", error);
                this.isLoading = false;
            }
        },
        async handleSearch(searchQuery) {
            this.searchPhrase = searchQuery
            this.getAdministrationRoutes();
        },
        async handlePageChange(newPage) {
            this.currentPage = newPage;
            this.getAdministrationRoutes();
        },
        async deleteAdministrationRoute(id) {
            this.isLoading = true;
            try {
                await deleteItem("administration_routes", id);
                const index = this.administration_routes.findIndex((administration_route) => administration_route.id === id);
                if (index !== -1) {
                    this.administration_routes.splice(index, 1);
                }
                this.showDeleteModal = false;
                this.isLoading = false;
            } catch (error) {
                console.error("Error fetching administration routes:", error);
                this.isLoading = false;
                this.showDeleteModal = false;
            }
        },
        showDeleteConfirmation(id) {
            this.deleteAdministrationRouteId = id;
            this.showDeleteModal = true;
        },
        cancelDelete() {
            this.showDeleteModal = false;
        },
        getRowClass(index) {
            return index % 2 === 0 ? 'bg-athens-gray-400' : 'bg-athens-gray-100';
        },
    }
}
</script>