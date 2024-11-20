const {
    merge
} = window._;

// form config.js
const echartSetOption = (
    chart,
    userOptions,
    getDefaultOptions,
    responsiveOptions
) => {
    const {
        breakpoints,
        resize
    } = window.phoenix.utils;
    const handleResize = options => {
        Object.keys(options).forEach(item => {
            if (window.innerWidth > breakpoints[item]) {
                chart.setOption(options[item]);
            }
        });
    };

    const themeController = document.body;
    // Merge user options with lodash
    chart.setOption(merge(getDefaultOptions(), userOptions));

    const navbarVerticalToggle = document.querySelector(
        '.navbar-vertical-toggle'
    );
    if (navbarVerticalToggle) {
        navbarVerticalToggle.addEventListener('navbar.vertical.toggle', () => {
            chart.resize();
            if (responsiveOptions) {
                handleResize(responsiveOptions);
            }
        });
    }

    resize(() => {
        chart.resize();
        if (responsiveOptions) {
            handleResize(responsiveOptions);
        }
    });
    if (responsiveOptions) {
        handleResize(responsiveOptions);
    }

    themeController.addEventListener(
        'clickControl',
        ({
            detail: {
                control
            }
        }) => {
            if (control === 'phoenixTheme') {
                chart.setOption(window._.merge(getDefaultOptions(), userOptions));
            }
        }
    );
};

const tooltipFormatter = (params, dateFormatter = 'MMM DD') => {
    let tooltipItem = ``;
    params.forEach(el => {
        tooltipItem += `<div class='ms-1'>
          <h6 class="text-body-tertiary"><span class="fas fa-circle me-1 fs-10" style="color:${el.borderColor ? el.borderColor : el.color
            }"></span>
            ${el.seriesName} : ${typeof el.value === 'object' ? el.value[1] : el.value
            }
          </h6>
        </div>`;
    });
    return `<div>
              <p class='mb-2 text-body-tertiary'>
                ${window.dayjs(params[0].axisValue).isValid()
            ? window.dayjs(params[0].axisValue).format(dateFormatter)
            : params[0].axisValue
        }
              </p>
              ${tooltipItem}
            </div>`;
};