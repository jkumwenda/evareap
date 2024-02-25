<template>
    <div class="flex flex-col space-y-4 flex-1">
        <HeaderView :headerTitle="headerTitle"></HeaderView>

        <SpinnerComponent v-if="isLoading" />

        <div v-else class="flex flex-row space-x-2">
            <div class="flex flex-col space-y-3 w-6/12 rounded-2xl bg-catskill-white-100 shadow-sm p-4">
                <div class="flex flex-row">
                    <h1 class="flex flex-1 items-center font-bold uppercase text-catalina-blue-500">Workflows</h1>
                    <div
                        class="mt-2 px-4 py-1 text-catskill-white-100 bg-catalina-blue hover:bg-catalina-blue-400 rounded-xl">
                        Add workflow</div>
                </div>
                <div class="flex flex-1 p-2 text-sm items-center bg-athens-gray-400 rounded-2xl"
                    v-for="workflow in workflows" :key="workflow.id">
                    <div class="w-11/12">{{ workflow.workflow }}</div>
                    <div class="flex space-x-2">
                        <router-link :to="{ name: 'Workflow', params: { id: workflow.id } }"
                            v-if="permissions.includes('VIEW_WORKFLOW')"
                            class="p-1 bg-dodger-blue-50 border border-catalina-blue-300 rounded-full">
                            <EyeIcon class="w-5 h-5 text-catalina-blue-300"></EyeIcon>
                        </router-link>
                        <div v-if="permissions.includes('UPDATE_WORKFLOW')"
                            class="p-1 bg-spray-200 border border-spray-700 rounded-full">
                            <PencilSquareIcon class=" w-5 h-5 text-spray-700">
                            </PencilSquareIcon>
                        </div>
                        <div v-if="permissions.includes('DELETE_WORKFLOW')"
                            class="p-1 bg-flamingo-100 border border-flamingo-500 rounded-full">
                            <TrashIcon class="w-5 h-5 text-flamingo-500" @click="showDeleteConfirmation(workflow.id)">
                            </TrashIcon>
                        </div>
                    </div>
                </div>
            </div>
            <div class="w-6/12 rounded-2xl bg-catskill-white-100 shadow-sm p-4">
                <div class="flex flex-row">
                    <h1 class="flex flex-1 items-center font-bold uppercase text-catalina-blue-500">Workflow stages</h1>
                    <div
                        class="mt-2 px-4 py-1 text-catskill-white-100 bg-catalina-blue hover:bg-catalina-blue-400 rounded-xl">
                        Add stage</div>
                </div>
                <div>{{ workflow }}</div>
            </div>
        </div>
        <delete-confirmation-modal :show="showDeleteModal" @confirmed="deleteWorkflow(deleteWorkflowId)"
            @canceled="cancelDelete"></delete-confirmation-modal>
    </div>
</template>

<script>
import HeaderView from '@/includes/Header.vue'
import { EyeIcon, PencilSquareIcon, TrashIcon } from '@heroicons/vue/24/solid'
import { fetchData, deleteItem, fetchItem } from "@/services/apiService";
import SpinnerComponent from "@/components/Spinner.vue";
import DeleteConfirmationModal from "@/components/DeleteConfirmationModal.vue";
import { useAuthStore } from "@/store/authStore";

export default {
    name: 'WorkflowsView',
    components: {
        HeaderView, SpinnerComponent, DeleteConfirmationModal, EyeIcon, PencilSquareIcon, TrashIcon
    },
    data() {
        return {
            headerTitle: "Workflows",
            id: this.$route.params.id,
            workflows: {},
            workflow: "",
            isLoading: true,
            showDeleteModal: false,
            deletePersonnelId: null,
            currentPage: 1,
            totalPages: "",
            pageSize: process.env.VUE_APP_PAGE_SIZE,
            searchPhrase: ""
        };
    },
    watch: {
        '$route.params.id': {
            immediate: true, // Trigger the watcher immediately on component mount
            handler(newId, oldId) {
                if (newId !== oldId) {
                    // ID has changed, update the workflow data
                    this.id = newId;
                    this.getWorkflow();
                }
            },
        },
    },
    mounted() {
        this.getWorkflows();
        this.getWorkflow();
    },
    setup() {
        const authStore = useAuthStore()
        const permissions = authStore.permissions
        return { permissions }
    },
    methods: {
        async getWorkflows() {
            try {
                const response = await fetchData("workflows", this.currentPage, this.pageSize, this.searchPhrase);
                this.workflows = response.data;
                this.totalPages = response.pages;
                this.isLoading = false;
            } catch (error) {
                console.error("Error fetching workflows:", error);
                this.isLoading = false;
            }
        },
        async getWorkflow() {
            if (this.id) {
                console.log("Workflow ID:", this.id);
                try {
                    const response = await fetchItem("workflow", this.id);
                    this.workflow = response.data
                    this.isLoading = false;
                } catch (error) {
                    console.error("Error fetching role:", error);
                    this.isLoading = false;
                }
            } else {
                console.log("No workflow ID provided");
            }
        },
        async handleSearch(searchQuery) {
            this.searchPhrase = searchQuery
            this.getWorkflows();
        },
        async handlePageChange(newPage) {
            this.currentPage = newPage;
            this.getWorkflows();
        },
        async deleteWorkflow(id) {
            this.isLoading = true;
            try {
                await deleteItem("workflows", id);
                const index = this.workflows.findIndex((workflow) => workflow.id === id);
                if (index !== -1) {
                    this.workflows.splice(index, 1);
                }
                this.showDeleteModal = false;
                this.isLoading = false;
            } catch (error) {
                console.error("Error fetching workflows:", error);
                this.isLoading = false;
                this.showDeleteModal = false;
            }
        },
        showDeleteConfirmation(id) {
            this.deleteWorkflowId = id;
            this.showDeleteModal = true;
        },
        cancelDelete() {
            this.showDeleteModal = false;
        },
    }
}
</script>