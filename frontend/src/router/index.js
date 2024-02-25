import { createRouter, createWebHashHistory } from "vue-router";
import AuthLayout from "@/layouts/AuthLayout.vue";
import MainLayout from "@/layouts/MainLayout.vue";
import NotFoundView from "@/views/NotFound.vue";

const routeComponents = {
  AuthLayout,
  MainLayout,
  LoginView: () => import("@/views/auth/Login.vue"),
  RegisterView: () => import("@/views/auth/Register.vue"),
  DashboardView: () => import("@/views/main/dashboard/Dashboard.vue"),
  PracticingLicensesView: () =>
    import("@/views/main/registrations/practicing/PracticingLicenses.vue"),
  RegisterPracticingLicenseView: () =>
    import(
      "@/views/main/registrations/practicing/RegisterPracticingLicense.vue"
    ),
  YourRegistrationView: () =>
    import("@/views/main/registrations/YourRegistration.vue"),
  ProductsView: () =>
    import("@/views/main/registrations/products/Products.vue"),
  AddProductView: () => import("@/views/main/registrations/products/Add.vue"),
  ProductView: () => import("@/views/main/registrations/products/Product.vue"),
  EditProductView: () => import("@/views/main/registrations/products/Edit.vue"),

  ApplicantsView: () => import("@/views/main/applicants/Applicants.vue"),
  AddApplicantView: () => import("@/views/main/applicants/Add.vue"),
  ApplicantView: () => import("@/views/main/applicants/Applicant.vue"),
  EditApplicantView: () => import("@/views/main/applicants/Edit.vue"),

  ManufacturersView: () =>
    import("@/views/main/manufacturers/Manufacturers.vue"),
  AddManufacturerView: () => import("@/views/main/manufacturers/Add.vue"),
  ManufacturerView: () => import("@/views/main/manufacturers/Manufacturer.vue"),
  EditManufacturerView: () => import("@/views/main/manufacturers/Edit.vue"),

  RegisterProductLicenseView: () =>
    import("@/views/main/registrations/products/RegisterProductLicense.vue"),
  BusinessesView: () =>
    import("@/views/main/registrations/businesses/Businesses.vue"),

  UsersView: () => import("@/views/main/configurations/users/Users.vue"),
  AddUserView: () => import("@/views/main/configurations/users/Add.vue"),
  UserView: () => import("@/views/main/configurations/users/User.vue"),
  EditUserView: () => import("@/views/main/configurations/users/Edit.vue"),

  RolesView: () => import("@/views/main/configurations/roles/Roles.vue"),
  AddRoleView: () => import("@/views/main/configurations/roles/Add.vue"),
  RoleView: () => import("@/views/main/configurations/roles/Role.vue"),
  EditRoleView: () => import("@/views/main/configurations/roles/Edit.vue"),

  ProductLicenceFeesView: () =>
    import(
      "@/views/main/configurations/product-licence-fees/ProductLicenceFees.vue"
    ),
  AddProductLicenceFeeView: () =>
    import("@/views/main/configurations/product-licence-fees/Add.vue"),
  EditProductLicenceFeeView: () =>
    import("@/views/main/configurations/product-licence-fees/Edit.vue"),

  ProductCategoriesView: () =>
    import(
      "@/views/main/configurations/product-categories/ProductCategories.vue"
    ),
  AddProductCategoryView: () =>
    import("@/views/main/configurations/product-categories/Add.vue"),
  EditProductCategoryView: () =>
    import("@/views/main/configurations/product-categories/Edit.vue"),

  TherapeuticCategoriesView: () =>
    import(
      "@/views/main/configurations/therapeutic-categories/TherapeuticCategories.vue"
    ),
  AddTherapeuticCategoryView: () =>
    import("@/views/main/configurations/therapeutic-categories/Add.vue"),
  EditTherapeuticCategoryView: () =>
    import("@/views/main/configurations/therapeutic-categories/Edit.vue"),

  AdministrationRoutesView: () =>
    import(
      "@/views/main/configurations/administration-routes/AdministrationRoutes.vue"
    ),
  AddAdministrationRouteView: () =>
    import("@/views/main/configurations/administration-routes/Add.vue"),
  EditAdministrationRouteView: () =>
    import("@/views/main/configurations/administration-routes/Edit.vue"),

  GenericNamesView: () =>
    import("@/views/main/configurations/generic-names/GenericNames.vue"),
  AddGenericNameView: () =>
    import("@/views/main/configurations/generic-names/Add.vue"),
  EditGenericNameView: () =>
    import("@/views/main/configurations/generic-names/Edit.vue"),

  DosageFormsView: () =>
    import("@/views/main/configurations/dosage-forms/DosageForms.vue"),
  AddDosageFormView: () =>
    import("@/views/main/configurations/dosage-forms/Add.vue"),
  EditDosageFormView: () =>
    import("@/views/main/configurations/dosage-forms/Edit.vue"),

  WorkflowsView: () =>
    import("@/views/main/configurations/workflows/Workflows.vue"),

  ConfigurationsView: () =>
    import("@/views/main/configurations/Configurations.vue"),
};

// Define your route configurations
const routes = [
  {
    path: "/",
    name: "Auth",
    component: routeComponents.AuthLayout,
    children: [
      {
        path: "/",
        name: "Login",
        component: routeComponents.LoginView,
      },
      {
        path: "/register",
        name: "Register",
        component: routeComponents.RegisterView,
      },
    ],
  },
  {
    path: "/",
    name: "Main",
    component: routeComponents.MainLayout,
    children: [
      {
        path: "/dashboard",
        name: "Dashboard",
        component: routeComponents.DashboardView,
      },
      {
        path: "/practicing-licenses",
        name: "PracticingLicenses",
        component: routeComponents.PracticingLicensesView,
      },
      {
        path: "/register-practicing-license",
        name: "RegisterPracticingLicense",
        component: routeComponents.RegisterPracticingLicenseView,
      },
      {
        path: "/your-registration",
        name: "YourRegistration",
        component: routeComponents.YourRegistrationView,
      },
      {
        path: "/products",
        name: "Products",
        component: routeComponents.ProductsView,
      },
      {
        path: "/add-product",
        name: "AddProduct",
        component: routeComponents.AddProductView,
      },
      {
        path: "/product/:id",
        name: "Product",
        component: routeComponents.ProductView,
      },
      {
        path: "/edit-product/:id",
        name: "EditProduct",
        component: routeComponents.EditProductView,
      },

      {
        path: "/applicants",
        name: "Applicants",
        component: routeComponents.ApplicantsView,
      },
      {
        path: "/add-applicant",
        name: "AddApplicant",
        component: routeComponents.AddApplicantView,
      },
      {
        path: "/applicant/:id",
        name: "Applicant",
        component: routeComponents.ApplicantView,
      },
      {
        path: "/edit-applicant/:id",
        name: "EditApplicant",
        component: routeComponents.EditApplicantView,
      },

      {
        path: "/manufacturers",
        name: "Manufacturers",
        component: routeComponents.ManufacturersView,
      },
      {
        path: "/add-applicant",
        name: "AddManufacturer",
        component: routeComponents.AddManufacturerView,
      },
      {
        path: "/manufacturer/:id",
        name: "Manufacturer",
        component: routeComponents.ManufacturerView,
      },
      {
        path: "/edit-manufacturer/:id",
        name: "EditManufacturer",
        component: routeComponents.EditManufacturerView,
      },

      {
        path: "/register-product-license",
        name: "RegisterProductLicense",
        component: routeComponents.RegisterProductLicenseView,
      },

      {
        path: "/businesses",
        name: "Businesses",
        component: routeComponents.BusinessesView,
      },

      {
        path: "/users",
        name: "Users",
        component: routeComponents.UsersView,
      },
      {
        path: "/add-user",
        name: "AddUser",
        component: routeComponents.AddUserView,
      },
      {
        path: "/user/:id",
        name: "User",
        component: routeComponents.UserView,
      },
      {
        path: "/edit-user/:id",
        name: "EditUser",
        component: routeComponents.EditUserView,
      },

      {
        path: "/roles",
        name: "Roles",
        component: routeComponents.RolesView,
      },
      {
        path: "/add-role",
        name: "AddRole",
        component: routeComponents.AddRoleView,
      },
      {
        path: "/role/:id",
        name: "Role",
        component: routeComponents.RoleView,
      },
      {
        path: "/edit-role/:id",
        name: "EditRole",
        component: routeComponents.EditRoleView,
      },

      {
        path: "/product-categories",
        name: "ProductCategories",
        component: routeComponents.ProductCategoriesView,
      },
      {
        path: "/add-product-category",
        name: "AddProductCategory",
        component: routeComponents.AddProductCategoryView,
      },
      {
        path: "/edit-product-category/:id",
        name: "EditProductCategory",
        component: routeComponents.EditProductCategoryView,
      },

      {
        path: "/therapeutic-categories",
        name: "TherapeuticCategories",
        component: routeComponents.TherapeuticCategoriesView,
      },
      {
        path: "/add-therapeutic-category",
        name: "AddTherapeuticCategory",
        component: routeComponents.AddTherapeuticCategoryView,
      },
      {
        path: "/edit-therapeutic-category/:id",
        name: "EditTherapeuticCategory",
        component: routeComponents.EditTherapeuticCategoryView,
      },

      {
        path: "/administration-routes",
        name: "AdministrationRoutes",
        component: routeComponents.AdministrationRoutesView,
      },
      {
        path: "/add-administration-route",
        name: "AddAdministrationRoute",
        component: routeComponents.AddAdministrationRouteView,
      },
      {
        path: "/edit-administration-route/:id",
        name: "EditAdministrationRoute",
        component: routeComponents.EditAdministrationRouteView,
      },

      {
        path: "/generic-names",
        name: "GenericNames",
        component: routeComponents.GenericNamesView,
      },
      {
        path: "/add-generic-name",
        name: "AddGenericName",
        component: routeComponents.AddGenericNameView,
      },
      {
        path: "/edit-generic-name/:id",
        name: "EditGenericName",
        component: routeComponents.EditGenericNameView,
      },

      {
        path: "/dosage-forms",
        name: "DosageForms",
        component: routeComponents.DosageFormsView,
      },
      {
        path: "/add-dosage-form",
        name: "AddDosageForm",
        component: routeComponents.AddDosageFormView,
      },
      {
        path: "/edit-dosage-form/:id",
        name: "EditDosageForm",
        component: routeComponents.EditDosageFormView,
      },

      {
        path: "/workflows",
        name: "Workflows",
        component: routeComponents.WorkflowsView,
      },
      {
        path: "/workflow/:id",
        name: "Workflow",
        component: routeComponents.WorkflowsView,
      },

      {
        path: "/product-licence-fees",
        name: "ProductLicenceFees",
        component: routeComponents.ProductLicenceFeesView,
      },
      {
        path: "/add-product-licence-fee",
        name: "AddProductLicenceFee",
        component: routeComponents.AddProductLicenceFeeView,
      },
      {
        path: "/product-licence-fee/:id",
        name: "ProductLicenceFee",
        component: routeComponents.ProductLicenceFeeView,
      },
      {
        path: "/edit-product-licence-fee/:id",
        name: "EditProductLicenceFee",
        component: routeComponents.EditProductLicenceFeeView,
      },

      {
        path: "/configurations",
        name: "Configurations",
        component: routeComponents.ConfigurationsView,
      },
    ],
  },
  { path: "/:catchAll(.*)", name: "NotFound", component: NotFoundView },
];

// Create the router instance
const router = createRouter({
  history: createWebHashHistory(process.env.BASE_URL),
  routes,
});

export default router;
