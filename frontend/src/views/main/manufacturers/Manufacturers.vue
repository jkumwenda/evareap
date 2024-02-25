<template>
    <div class="flex flex-col space-y-4 flex-1">
        <HeaderView :headerTitle="headerTitle"></HeaderView>
        <div class="flex flex-col space-y-4">
            <div class="flex justify-between items-center">
                <search-component @search="handleSearch"></search-component>
                <router-link :to="{ name: 'AddManufacturer' }" v-if="permissions.includes('ADD_MANUFACTURER')"
                    class="mt-2 px-4 py-2 text-catskill-white-100 bg-gradient-to-r from-catalina-blue-300 to-catalina-blue-500 hover:from-catalina-blue-400 hover:to-catalina-blue-600 rounded-xl">
                    Add Manufacturer</router-link>
            </div>
            <SpinnerComponent v-if="isLoading" />
            <div v-else class="rounded-2xl bg-catskill-white-100 shadow-sm p-4">
                <div class="flex flex-row bg-athens-gray-500 p-2 text-sm font-bold">
                    <div class="sm:w-3/12">Manufacturer</div>
                    <div class="sm:w-3/12">Address</div>
                    <div class="sm:w-2/12">Country</div>
                    <div class="sm:w-2/12">Phone</div>
                    <div class="sm:w-2/12">Email</div>
                    <div class="sm:w-1/12">Action</div>
                </div>
                <div class="flex flex-row p-2 text-sm items-center" v-for="(manufacturer, index) in manufacturers"
                    :key="manufacturer.id" :class="getRowClass(index)">
                    <div class="sm:w-3/12">{{ manufacturer.manufacturer }}</div>
                    <div class="sm:w-3/12">{{ manufacturer.address }}</div>
                    <div class="sm:w-2/12">{{ manufacturer.country.country }}</div>
                    <div class="sm:w-2/12">{{ manufacturer.phone }}</div>
                    <div class="sm:w-2/12">{{ manufacturer.email }}</div>
                    <div class="flex space-x-2 sm:w-1/12">
                        <router-link v-if="permissions.includes('VIEW_MANUFACTURER')"
                            class="p-1 bg-dodger-blue-50 rounded-full"
                            :to="{ name: 'Manufacturer', params: { id: manufacturer.id } }">
                            <EyeIcon class="w-5 h-5 text-catalina-blue-300"></EyeIcon>
                        </router-link>
                        <router-link v-if="permissions.includes('UPDATE_MANUFACTURER')"
                            class="p-1 bg-spray-200 rounded-full"
                            :to="{ name: 'EditManufacturer', params: { id: manufacturer.id } }">
                            <PencilSquareIcon class=" w-5 h-5 text-spray-700">
                            </PencilSquareIcon>
                        </router-link>
                        <div v-if="permissions.includes('DELETE_MANUFACTURER')" class="p-1 bg-flamingo-100 rounded-full">
                            <TrashIcon class="w-5 h-5 text-flamingo-500" @click="showDeleteConfirmation(manufacturer.id)">
                            </TrashIcon>
                        </div>
                    </div>
                </div>
                <pagination-component :currentPage="currentPage" :totalPages="totalPages" @page-change="handlePageChange">
                </pagination-component>
            </div>
        </div>
        <delete-confirmation-modal :show="showDeleteModal" @confirmed="deleteManufacturer(deleteManufacturerId)"
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
    name: 'ManufacturersView',
    components: {
        EyeIcon, PencilSquareIcon, TrashIcon, PaginationComponent, SearchComponent, HeaderView, SpinnerComponent, DeleteConfirmationModal
    },
    data() {
        return {
            headerTitle: "Manufacturers",
            manufacturers: {},
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
        this.getManufacturers();
    },
    setup() {
        const authStore = useAuthStore()
        const permissions = authStore.permissions
        return { permissions }
    },
    methods: {
        async getManufacturers() {
            try {
                const response = await fetchData("manufacturers", this.currentPage, this.pageSize, this.searchPhrase);
                this.manufacturers = response.data;
                this.totalPages = response.pages;
                this.isLoading = false;
            } catch (error) {
                console.error("Error fetching manufacturers:", error);
                this.isLoading = false;
            }
        },
        async handleSearch(searchQuery) {
            this.searchPhrase = searchQuery
            this.getManufacturers();
        },
        async handlePageChange(newPage) {
            this.currentPage = newPage;
            this.getManufacturers();
        },
        async deleteManufacturer(id) {
            this.isLoading = true;
            try {
                await deleteItem("manufacturers", id);
                const index = this.manufacturers.findIndex((manufacturer) => manufacturer.id === id);
                if (index !== -1) {
                    this.manufacturers.splice(index, 1);
                }
                this.showDeleteModal = false;
                this.isLoading = false;
            } catch (error) {
                console.error("Error fetching manufacturers:", error);
                this.isLoading = false;
                this.showDeleteModal = false;
            }
        },
        showDeleteConfirmation(id) {
            this.deleteManufacturerId = id;
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