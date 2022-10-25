"use strict";

const BASE_URL = "http://localhost:5000/api/cupcakes";

const $cupcakesList = $("#cupcake-list");
const $cupcakeForm = $("#cupcake-form");
const $cupcakeFormFlavor = $("#cupcake-form-flavor");
const $cupcakeFormSize = $("#cupcake-form-size");
const $cupcakeFormRating = $("#cupcake-form-rating");
const $cupcakeFormImage = $("#cupcake-form-image");

$cupcakeForm.on("submit", handleAddCupcake);

/**
 * Add event listener to the document to get all cupcakes
 */
document.addEventListener("DOMContentLoaded", async function () {
  emptyCupcakesList();
  const cupcakes = await getAllCupcakes();
  addAndMakeCupcakeElements(cupcakes);
});

/**
 * Add cupcake to database and refresh the cupcake list
 */
async function handleAddCupcake(evt) {
  evt.preventDefault();

  const flavor = $cupcakeFormFlavor.val();
  const size = $cupcakeFormSize.val();
  const rating = $cupcakeFormRating.val();
  const image = $cupcakeFormImage.val();

  const {
    data: { cupcake },
  } = await axios.post(BASE_URL, { flavor, size, rating, image });

  $cupcakesList.append(makeCupcakeElement(cupcake));
}

/**
 * Make and return a cupcake HTML element
 * Takes a cupcake
 */
function makeCupcakeElement(cupcake) {
  const $div = $("<div>");
  const $li = $("<li>");
  $li.text(
    `Size: ${cupcake.size} flavor: ${cupcake.flavor} rating: ${cupcake.rating}`
  );
  $li.attr("id", cupcake.id);
  const $image = $("<img>");
  $image.attr("src", cupcake.image);
  $div.append($li);
  $div.append($image);
  return $div;
}

/**
 * Get all cupcakes from API and add to DOM
 */
async function getAllCupcakes() {
  const {
    data: { cupcakes },
  } = await axios.get(BASE_URL);

  return cupcakes;
}

/**
 * Adds and make cupcake element divs to DOM
 * Takes a list of cupcakes
 */
function addAndMakeCupcakeElements(cupcakes) {
  const $cupcakeElements = cupcakes.map(makeCupcakeElement);
  $cupcakeElements.forEach((cupcake) => $cupcakesList.append(cupcake));
}

/**
 * Remove all cupcakes from DOM
 */
function emptyCupcakesList() {
  $cupcakesList.empty();
}
