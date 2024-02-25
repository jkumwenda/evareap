<template>
    <div class="flex flex-col space-y-4 flex-1">
        <HeaderView :headerTitle="headerTitle"></HeaderView>
        <div class="flex flex-col space-y-4">
            <div class="flex justify-between items-center">
                <search-component @search="handleSearch"></search-component>
                <router-link :to="{ name: 'AddDosageForm' }" v-if="permissions.includes('ADD_PRODUCT_CATEGORY')"
                    class="mt-2 px-4 py-2 text-catskill-white-100 bg-gradient-to-r from-catalina-blue-300 to-catalina-blue-500 hover:from-catalina-blue-400 hover:to-catalina-blue-600 rounded-xl">
                    Add Dosage form</router-link>
            </div>
            <SpinnerComponent v-if="isLoading" />
            <div v-else class="rounded-2xl bg-catskill-white-100 shadow-sm p-4">
                <div class="flex flex-row bg-athens-gray-500 p-2 text-sm font-bold">
                    <div class="sm:w-4/12">Dosage form</div>
                    <div class="sm:w-7/12">Description</div>
                    <div class="sm:w-1/12">Action</div>
                </div>
                <div class="flex flex-row p-2 text-sm items-center" v-for="(dosage_form, index) in dosage_forms"
                    :key="dosage_form.id" :class="getRowClass(index)">
                    <div class="sm:w-4/12">{{ dosage_form.dosage_form }}</div>
                    <div class="sm:w-7/12">{{ dosage_form.description }}</div>
                    <div class="flex space-x-2 sm:w-1/12">
                        <router-link v-if="permissions.includes('UPDATE_PRODUCT_CATEGORY')"
                            class="p-1 bg-spray-200 rounded-full"
                            :to="{ name: 'EditDosageForm', params: { id: dosage_form.id } }">
                            <PencilSquareIcon class=" w-5 h-5 text-spray-700">
                            </PencilSquareIcon>
                        </router-link>
                        <div v-if="permissions.includes('DELETE_PRODUCT_CATEGORY')"
                            class="p-1 bg-flamingo-100 rounded-full">
                            <TrashIcon class="w-5 h-5 text-flamingo-500" @click="showDeleteConfirmation(dosage_form.id)">
                            </TrashIcon>
                        </div>
                    </div>
                </div>
                <pagination-component :currentPage="currentPage" :totalPages="totalPages" @page-change="handlePageChange">
                </pagination-component>
            </div>
        </div>
        <delete-confirmation-modal :show="showDeleteModal" @confirmed="deleteDosageForm(deleteDosageFormId)"
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
    name: 'DosageFormsView',
    components: {
        PencilSquareIcon, TrashIcon, PaginationComponent, SearchComponent, HeaderView, SpinnerComponent, DeleteConfirmationModal
    },
    data() {
        return {
            headerTitle: "Dosage Form",
            dosage_forms: {},
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
        this.getDosageForms();
    },
    setup() {
        const authStore = useAuthStore()
        const permissions = authStore.permissions
        return { permissions }
    },
    methods: {
        async getDosageForms() {
            try {
                const response = await fetchData("dosage_forms", this.currentPage, this.pageSize, this.searchPhrase);
                this.dosage_forms = response.data;
                this.totalPages = response.pages;
                this.isLoading = false;
            } catch (error) {
                console.error("Error fetching dosage forms:", error);
                this.isLoading = false;
            }
        },
        async handleSearch(searchQuery) {
            this.searchPhrase = searchQuery
            this.getDosageForms();
        },
        async handlePageChange(newPage) {
            this.currentPage = newPage;
            this.getDosageForms();
        },
        async deleteDosageForm(id) {
            this.isLoading = true;
            try {
                await deleteItem("dosage_forms", id);
                const index = this.dosage_forms.findIndex((dosage_form) => dosage_form.id === id);
                if (index !== -1) {
                    this.dosage_forms.splice(index, 1);
                }
                this.showDeleteModal = false;
                this.isLoading = false;
            } catch (error) {
                console.error("Error fetching dosage forms:", error);
                this.isLoading = false;
                this.showDeleteModal = false;
            }
        },
        showDeleteConfirmation(id) {
            this.deleteDosageFormId = id;
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