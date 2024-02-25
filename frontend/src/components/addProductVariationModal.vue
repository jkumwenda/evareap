<template>
  <div v-if="show" class="fixed inset-0 flex items-center justify-center z-50">
    <div
      class="flex flex-col border-2 border-catalina-blue-500 border-t-8 bg-catskill-white-100 dark:bg-gray-800 rounded-xl shadow-lg w-6/12 z-50">
      <div class="border-b font-bold text-lg border-b-4 p-4 px-6 space-y-4 border-b-silver-500">
        Create Product variation
      </div>
      <div v-if="message" class="p-4 m-6 rounded-xl text-catskill-white-100 py-2 text bg-mountain-meadow-500">
        {{ message }}
      </div>
      <SpinnerComponent v-if="isLoading" />
      <form class="flex flex-col w-12/12 space-y-4 p-5" @submit.prevent="addProductVariation" method="POST">
        <div class="flex space-x-4">
          <label class="block w-6/12">
            <span class="after:content-['*'] after:ml-0.5 after:text-red-500 block text-sm font-medium text-slate-700">
              Product Category
            </span>
            <select name="product_category_id"
              class="mt-2 px-2 py-2 bg-white border border-1 shadow-sm border-mid-gray-300 placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-sky-500 block w-full rounded-xl sm:text-sm focus:ring-1"
              v-model="productVariationData.product_category_id">
              <option value="" disabled selected>--Select product category--</option>
              <option v-for="product_category in product_categories" :key="product_category.id"
                :value="product_category.id">
                {{ product_category.product_category }}
              </option>
            </select>
          </label>
        </div>
        <div class="flex space-x-4">
          <label class="block w-6/12">
            <span class="after:content-['*'] after:ml-0.5 after:text-red-500 block text-sm font-medium text-slate-700">
              Product name
            </span>
            <input type="input" name="product_name" v-model="productVariationData.product_name"
              class="mt-2 px-2 py-2 bg-white border border-1 shadow-sm border-mid-gray-300 placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-sky-500 block w-full rounded-xl sm:text-sm focus:ring-1"
              placeholder="Product name" />
          </label>
          <label class="block w-6/12">
            <span class="after:content-['*'] after:ml-0.5 after:text-red-500 block text-sm font-medium text-slate-700">
              Generic name
            </span>
            <select name="generic_name_id"
              class="mt-2 px-2 py-2 bg-white border border-1 shadow-sm border-mid-gray-300 placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-sky-500 block w-full rounded-xl sm:text-sm focus:ring-1"
              v-model="productVariationData.generic_name_id">
              <option value="" disabled selected>--Select generic names--</option>
              <option v-for="generic_name in generic_names" :key="generic_name.id" :value="generic_name.id">
                {{ generic_name.generic_name }}
              </option>
            </select>
          </label>
        </div>
        <div class="flex space-x-4">
          <label class="block w-6/12">
            <span class="after:content-['*'] after:ml-0.5 after:text-red-500 block text-sm font-medium text-slate-700">
              Dosage form
            </span>
            <select name="dosage_form_id"
              class="mt-2 px-2 py-2 bg-white border border-1 shadow-sm border-mid-gray-300 placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-sky-500 block w-full rounded-xl sm:text-sm focus:ring-1"
              v-model="productVariationData.dosage_form_id">
              <option value="" disabled selected>--Select dosage forms--</option>
              <option v-for="dosage_form in dosage_forms" :key="dosage_form.id" :value="dosage_form.id">
                {{ dosage_form.dosage_form }}
              </option>
            </select>
          </label>
          <label class="block w-6/12">
            <span class="after:content-['*'] after:ml-0.5 after:text-red-500 block text-sm font-medium text-slate-700">
              Therapeutic category
            </span>
            <select name="therapeutic_category_id"
              class="mt-2 px-2 py-2 bg-white border border-1 shadow-sm border-mid-gray-300 placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-sky-500 block w-full rounded-xl sm:text-sm focus:ring-1"
              v-model="productVariationData.therapeutic_category_id">
              <option value="" disabled selected>--Select therapeutic categories--</option>
              <option v-for="therapeutic_category in therapeutic_categories" :key="therapeutic_category.id"
                :value="therapeutic_category.id">
                {{ therapeutic_category.therapeutic_category }}
              </option>
            </select>
          </label>
        </div>

        <div class="flex space-x-4">
          <label class="block w-6/12">
            <span class="after:content-['*'] after:ml-0.5 after:text-red-500 block text-sm font-medium text-slate-700">
              Color
            </span>
            <input type="input" name="color" v-model="productVariationData.color"
              class="mt-2 px-2 py-2 bg-white border border-1 shadow-sm border-mid-gray-300 placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-sky-500 block w-full rounded-xl sm:text-sm focus:ring-1"
              placeholder="Color" />
          </label>
          <label class="block w-6/12">
            <span class="after:content-['*'] after:ml-0.5 after:text-red-500 block text-sm font-medium text-slate-700">
              Scheduling status
            </span>
            <input type="input" name="scheduling_status" v-model="productVariationData.scheduling_status"
              class="mt-2 px-2 py-2 bg-white border border-1 shadow-sm border-mid-gray-300 placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-sky-500 block w-full rounded-xl sm:text-sm focus:ring-1"
              placeholder="Scheduling status" />
          </label>
        </div>
        <div class="flex space-x-4">
          <label class="block w-6/12">
            <span class="after:content-['*'] after:ml-0.5 after:text-red-500 block text-sm font-medium text-slate-700">
              Strength
            </span>
            <input type="input" name="strength" v-model="productVariationData.strength"
              class="mt-2 px-2 py-2 bg-white border border-1 shadow-sm border-mid-gray-300 placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-sky-500 block w-full rounded-xl sm:text-sm focus:ring-1"
              placeholder="strength" />
          </label>
          <label class="block w-6/12">
            <span class="after:content-['*'] after:ml-0.5 after:text-red-500 block text-sm font-medium text-slate-700">
              Administrative route
            </span>
            <select name="administration_route_id"
              class="mt-2 px-2 py-2 bg-white border border-1 shadow-sm border-mid-gray-300 placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-sky-500 block w-full rounded-xl sm:text-sm focus:ring-1"
              v-model="productVariationData.administration_route_id">
              <option value="" disabled selected>--Select administration routes--</option>
              <option v-for="administration_route in administration_routes" :key="administration_route.id"
                :value="administration_route.id">
                {{ administration_route.administration_route }}
              </option>
            </select>
          </label>
        </div>

        <div class="flex space-x-4">
          <label class="block w-6/12">
            <span class="after:content-['*'] after:ml-0.5 after:text-red-500 block text-sm font-medium text-slate-700">
              Active ingredients
            </span>
            <input type="input" name="active_ingredient" v-model="productVariationData.active_ingredient"
              class="mt-2 px-2 py-2 bg-white border border-1 shadow-sm border-mid-gray-300 placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-sky-500 block w-full rounded-xl sm:text-sm focus:ring-1"
              placeholder="Active ingredients" />
          </label>
          <label class="block w-6/12">
            <span class="after:content-['*'] after:ml-0.5 after:text-red-500 block text-sm font-medium text-slate-700">
              Content /Unit dose
            </span>
            <input type="input" name="unit_dose" v-model="productVariationData.unit_dose"
              class="mt-2 px-2 py-2 bg-white border border-1 shadow-sm border-mid-gray-300 placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-sky-500 block w-full rounded-xl sm:text-sm focus:ring-1"
              placeholder="Unit dose" />
          </label>
        </div>

        <div class="flex space-x-4">
          <label class="block w-6/12">
            <span class="after:content-['*'] after:ml-0.5 after:text-red-500 block text-sm font-medium text-slate-700">
              Package size
            </span>
            <input type="input" name="package_size" v-model="productVariationData.package_size"
              class="mt-2 px-2 py-2 bg-white border border-1 shadow-sm border-mid-gray-300 placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-sky-500 block w-full rounded-xl sm:text-sm focus:ring-1"
              placeholder="Package size" />
          </label>
          <label class="block w-6/12">
            <span class="after:content-['*'] after:ml-0.5 after:text-red-500 block text-sm font-medium text-slate-700">
              Package type
            </span>
            <input type="input" name="package_type" v-model="productVariationData.package_type"
              class="mt-2 px-2 py-2 bg-white border border-1 shadow-sm border-mid-gray-300 placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-sky-500 block w-full rounded-xl sm:text-sm focus:ring-1"
              placeholder="package type" />
          </label>
        </div>

        <div class="flex space-x-4">
          <div class="flex flex-row space-x-4">
            <button type="submit"
              class="mt-2 px-4 py-2 text-catskill-white-100 bg-catalina-blue hover:bg-catalina-blue-400 rounded-xl">
              Add product variation
            </button>
            <button :to="{ name: 'Products' }" @click="close"
              class="mt-2 px-4 py-2 boder border-2 border-catalina-blue rounded-xl">Cancel</button>
          </div>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { createItem, fetchData } from "@/services/apiService";
import SpinnerComponent from "@/components/Spinner.vue";

export default {
  components: {
    SpinnerComponent
  },

  data() {
    return {
      headerTitle: "Product Registration",
      productVariationData: {
        product_id: "",
        product_category_id: "",
        product_name: "",
        generic_name_id: "",
        dosage_form_id: "",
        therapeutic_category_id: "",
        color: "",
        scheduling_status: "",
        strength: "",
        administration_route_id: "",
        manufacturer_id: "",
        country_id: "",
        active_ingredient: "",
        unit_dose: "",
        package_size: "",
        package_type: "",
      },
      isLoading: false,
      generic_names: {},
      dosage_forms: {},
      administration_routes: {},
      currentPage: 1,
      totalPages: "",
      pageSize: 500,
      searchPhrase: "",
      message: ""
    }
  },


  props: {
    show: {
      type: Boolean,
      required: true,
    },
    product: {
      type: Object,
      required: true,
    },
  },

  watch: {
    product: {
      immediate: true,
      handler(newValue) {
        this.productVariationData = { ...newValue };
        this.getProductCategories();
        this.getGenericNames();
        this.getDosageForms();
        this.getTherapeuticCategories();
        this.getAdministrativeRoutes();
      },
    },
  },

  async mounted() {

    await this.getProductCategories()
    await this.getGenericNames()
    await this.getDosageForms()
    await this.getTherapeuticCategories()
    await this.getAdministrativeRoutes()
  },
  methods: {
    async addProductVariation() {
      this.isLoading = true;
      try {
        const response = await createItem("products/add_product_variation", this.productVariationData);
        this.products = response.data;
        this.isLoading = false;
        this.$emit("product-approved");
        this.message = "Signature file uploaded successfully";
      } catch (error) {
        console.error("Error fetching products:", error);
        this.isLoading = false;
      }
    },
    async getProductCategories() {
      this.isLoading = true;
      try {
        const response = await fetchData("product_categories", this.currentPage, this.pageSize, this.searchPhrase);
        this.product_categories = response.data;
        this.isLoading = false;
      } catch (error) {
        console.error("Error fetching product categories:", error);
        this.isLoading = false;
      }
    },
    async getGenericNames() {
      this.isLoading = true;
      try {
        const response = await fetchData("generic_names", this.currentPage, this.pageSize, this.searchPhrase);
        this.generic_names = response.data;
        this.isLoading = false;
      } catch (error) {
        console.error("Error fetching generic names:", error);
        this.isLoading = false;
      }
    },
    async getDosageForms() {
      this.isLoading = true;
      try {
        const response = await fetchData("dosage_forms", this.currentPage, this.pageSize, this.searchPhrase);
        this.dosage_forms = response.data;
        this.isLoading = false;
      } catch (error) {
        console.error("Error fetching dosage forms:", error);
        this.isLoading = false;
      }
    },
    async getTherapeuticCategories() {
      this.isLoading = true;
      try {
        const response = await fetchData("therapeutic_categories", this.currentPage, this.pageSize, this.searchPhrase);
        this.therapeutic_categories = response.data;
        this.isLoading = false;
      } catch (error) {
        console.error("Error fetching therapeutic categories:", error);
        this.isLoading = false;
      }
    },
    async getAdministrativeRoutes() {
      this.isLoading = true;
      try {
        const response = await fetchData("administration_routes", this.currentPage, this.pageSize, this.searchPhrase);
        this.administration_routes = response.data;
        this.isLoading = false;
      } catch (error) {
        console.error("Error fetching administration routes:", error);
        this.isLoading = false;
      }
    },
    close() {
      this.$emit("closed");
    },

  },
};
</script>
