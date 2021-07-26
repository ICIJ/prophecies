<template>
  <div class="latest-tips-card card card-body py-4 px-5 shadow-lg">
    <div class="d-flex align-items-center mt-3 mb-5">
      <smile-icon class="text-primary mr-4" />
      <h2 class="latest-tips-card__title text-primary mb-0">
        Latest Tips
      </h2>
    </div>
    <ul class="list-unstyled latest-tips-card__tips">
      <li class="latest-tips-card__tips__item">
        <h3 class="latest-tips-card__tips__item__title">
          How should I decide between “the BVI” and “BVI”?
        </h3>
        <div class="d-flex">
          <div>
            <arrow-right-icon class="mr-3 text-primary" size="1.5x" />
          </div>
          <p class="flex-grow-1">
            Pick the BVI if it is the case xyz. In any other cases, please pick BVI.
          </p>
        </div>
      </li>
      <li class="latest-tips-card__tips__item">
        <h3 class="latest-tips-card__tips__item__title">
          Country is unknow, what should I do?
        </h3>
        <div class="d-flex">
          <div>
            <arrow-right-icon class="mr-3 text-primary" size="1.5x" />
          </div>
          <p class="flex-grow-1">
            Always FR, as all country codes. If you have any question, please contact me (Karrie)!
          </p>
        </div>
      </li>
    </ul>
  </div>
</template>

<style lang="scss" scoped>
  .latest-tips-card {

    &__title {
      position: relative;
      padding-bottom: $spacer;

      &:after {
        content: "";
        width: 100%;
        max-width: 120px;
        position: absolute;
        bottom: 0%;
        left: 0;
        height: 7px;
        background: $warning;
        font-weight: 600;
      }
    }

    &__tips {

      &__item {
        margin-bottom: $spacer-lg;

        &__title {
          font-weight: 600;
          margin-bottom: $spacer-lg;
        }
      }
    }
  }
</style>
