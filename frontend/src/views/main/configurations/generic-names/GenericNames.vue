<template>
    <div class="flex flex-col space-y-4 flex-1">
        <HeaderView :headerTitle="headerTitle"></HeaderView>
        <div class="flex flex-col space-y-4">
            <div class="flex justify-between items-center">
                <search-component @search="handleSearch"></search-component>
                <router-link :to="{ name: 'AddGenericName' }" v-if="permissions.includes('ADD_PRODUCT_CATEGORY')"
                    class="mt-2 px-4 py-2 text-catskill-white-100 bg-gradient-to-r from-catalina-blue-300 to-catalina-blue-500 hover:from-catalina-blue-400 hover:to-catalina-blue-600 rounded-xl">
                    Add Generic name</router-link>
            </div>
            <SpinnerComponent v-if="isLoading" />
            <div v-else class="rounded-2xl bg-catskill-white-100 shadow-sm p-4">
                <div class="flex flex-row bg-athens-gray-500 p-2 text-sm font-bold">
                    <div class="sm:w-4/12">Generic name</div>
                    <div class="sm:w-7/12">Description</div>
                    <div class="sm:w-1/12">Action</div>
                </div>
                <div class="flex flex-row p-2 text-sm items-center" v-for="(generic_name, index) in generic_names"
                    :key="generic_name.id" :class="getRowClass(index)">
                    <div class="sm:w-4/12">{{ generic_name.generic_name }}</div>
                    <div class="sm:w-7/12">{{ generic_name.description }}</div>
                    <div class="flex space-x-2 sm:w-1/12">
                        <router-link v-if="permissions.includes('UPDATE_PRODUCT_CATEGORY')"
                            class="p-1 bg-spray-200 rounded-full"
                            :to="{ name: 'EditGenericName', params: { id: generic_name.id } }">
                            <PencilSquareIcon class=" w-5 h-5 text-spray-700">
                            </PencilSquareIcon>
                        </router-link>
                        <div v-if="permissions.includes('DELETE_PRODUCT_CATEGORY')"
                            class="p-1 bg-flamingo-100 rounded-full">
                            <TrashIcon class="w-5 h-5 text-flamingo-500" @click="showDeleteConfirmation(generic_name.id)">
                            </TrashIcon>
                        </div>
                    </div>
                </div>
                <pagination-component :currentPage="currentPage" :totalPages="totalPages" @page-change="handlePageChange">
                </pagination-component>
            </div>
        </div>
        <delete-confirmation-modal :show="showDeleteModal" @confirmed="deleteGenericName(deleteGenericNameId)"
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
    name: 'GenericNamesView',
    components: {
        PencilSquareIcon, TrashIcon, PaginationComponent, SearchComponent, HeaderView, SpinnerComponent, DeleteConfirmationModal
    },
    data() {
        return {
            headerTitle: "Generic Name",
            generic_names: {},
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
        this.getGenericNames();
    },
    setup() {
        const authStore = useAuthStore()
        const permissions = authStore.permissions
        return { permissions }
    },
    methods: {
        async getGenericNames() {
            try {
                const response = await fetchData("generic_names", this.currentPage, this.pageSize, this.searchPhrase);
                this.generic_names = response.data;
                this.totalPages = response.pages;
                this.isLoading = false;
            } catch (error) {
                console.error("Error fetching generic names:", error);
                this.isLoading = false;
            }
        },
        async handleSearch(searchQuery) {
            this.searchPhrase = searchQuery
            this.getGenericNames();
        },
        async handlePageChange(newPage) {
            this.currentPage = newPage;
            this.getGenericNames();
        },
        async deleteGenericName(id) {
            this.isLoading = true;
            try {
                await deleteItem("generic_names", id);
                const index = this.generic_names.findIndex((generic_name) => generic_name.id === id);
                if (index !== -1) {
                    this.generic_names.splice(index, 1);
                }
                this.showDeleteModal = false;
                this.isLoading = false;
            } catch (error) {
                console.error("Error fetching generic names:", error);
                this.isLoading = false;
                this.showDeleteModal = false;
            }
        },
        showDeleteConfirmation(id) {
            this.deleteGenericNameId = id;
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