<template>
  <div class="flex flex-col space-y-4 flex-1">
    <HeaderView :headerTitle="headerTitle"></HeaderView>
    <SpinnerComponent v-if="isLoading" />
    <div v-else class="rounded-2xl bg-catskill-white-100 shadow-sm p-4">
      <form class="flex flex-col w-5/12 space-y-4" @submit.prevent="editProductLicenceFee" method="POST">
        <label class="block">
          <span class="after:content-['*'] after:ml-0.5 after:text-red-500 block text-sm font-medium text-slate-700">
            Product Licence Fee
          </span>
          <input type="input" name="product_license_fee" v-model="productLicenceFeeData.product_license_fee"
            class="mt-2 px-3 py-3 bg-white border border-1 shadow-sm border-mid-gray-300 placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-sky-500 block w-full rounded-xl sm:text-sm focus:ring-1"
            placeholder="Product licence fee" />
        </label>
        <div class="flex flex-row space-x-4">
          <button type="submit"
            class="mt-2 px-4 py-2 text-catskill-white-100 bg-catalina-blue hover:bg-catalina-blue-400 rounded-xl">
            Edit product licence fee
          </button>
          <router-link :to="{ name: 'ProductLicenceFees' }"
            class="mt-2 px-4 py-2 boder border-2 border-catalina-blue rounded-xl">Cancel</router-link>
        </div>
      </form>
    </div>
  </div>
</template>
<script>
import { updateItem, fetchItem } from "@/services/apiService";
import HeaderView from '@/includes/Header.vue'
import SpinnerComponent from "@/components/Spinner.vue";
import router from "@/router";

export default {
  name: "EditProductLicenceFeeView",
  components: {
    HeaderView, SpinnerComponent
  },
  data() {
    return {
      headerTitle: "Edit product licence fee",
      id: this.$route.params.id,
      productLicenceFeeData: {
        product_license_fee: "",
      },
      isLoading: false,
      product_licence_fee: {},
    };
  },
  mounted() {
    this.getProductLicenceFee();
  },
  methods: {
    async editProductLicenceFee() {
      this.isLoading = true;
      try {
        const response = await updateItem(
          "product_licence_fees",
          this.id,
          this.productLicenceFeeData
        );
        this.product_licence_fee = response.data;
        this.isLoading = false;
        router.push("/product-licence-fees");
      } catch (error) {
        console.error("Error editing product licence fee:", error);
        this.isLoading = false;
      }
    },
    async getProductLicenceFee() {
      try {
        const response = await fetchItem("product_licence_fees", this.id);
        console.log(response)
        this.productLicenceFeeData.product_license_fee = response.product_licence_fee.product_licence_fee;
        this.isLoading = false;
      } catch (error) {
        console.error("Error fetching product licence fee:", error);
        this.isLoading = false;
      }
    },
  },
};
</script>
