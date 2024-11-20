class Reset {
    reset() {
        let elements = this.elements;
        for (let key in elements) {
            if (elements.hasOwnProperty(key)) {
                let ele = elements[key];
                if(ele){
                    if(ele instanceof Choices){
                        if (ele.passedElement.element.hasAttribute("multiple")) {
                            ele?.removeActiveItems();
                        } else {
                            ele?.setChoiceByValue("");
                        }
                    }else{
                        ele.value = ''
                    }
                }
            }
        }
        let listData = this.form.querySelectorAll('[class*="set"]');
        listData.forEach(element => {
            let classes = element.className.split(' ');
            classes.forEach(cls => {
                if (cls.includes('set')) {
                    let dataSet = cls.split('-');
                    if (dataSet.length > 1 && dataSet[0] == 'set') {
                        let checkChoice = element.hasAttribute("data-choice") ? true : false;
                        if (checkChoice) {
                            let nameSelect = element.getAttribute('name');
                            this.elements[nameSelect]?.setChoiceByValue(String(dataSet[1]));
                        } else {
                            element.value = dataSet[1];
                        }
                    }
                }
            });
        });
        removeAllValidationClasses(this.form);
    }
}

class Validator {
    static required(value){
        if(Array.isArray(value)){
            return value.length <= 0 ? 'là trưởng bắt buộc' : '';
        }
        return value.trim() == '' ? 'là trường bắt buộc' : '';
    }
    static price(value) {
        const regex = /^\d{1,3}(,\d{3})*(\.\d+)?$/;
        return regex.test(value) ? '' : 'không đúng định dạng tiền';
    }
    static min(value,vl){
        if (typeof value === 'string') {
            value = parseFloat(value.replace(/,/g, ''));
        }
        return value < vl ? `giá trị tối thiểu là ${vl}` : '';
    }
    static max(value,vl){
        if (typeof value === 'string') {
            value = parseFloat(value.replace(/,/g, ''));
        }
        return value > vl ? `giá trị tối đa là ${vl}` : '';
    }
}

class Form extends Reset {
    data = {};
    elements = {};
    validate = {};
    submit = () => { };
    errors = {};

    constructor() {
        super();
    }

    removeValidate(string){
        let data = string.split('.')
        this.validate[data[0]] = this.validate[data[0]].filter(val => val != data[1]); 
    }

    setValidate() {
        for (let key in this.elements) {
            this.validate[key] = ['required'];
            this.errors[key] = {
                attribute: key,
                messages: [],
            };
        }
        this.startValidate();
    }

    startValidate() {
        for (let key in this.elements) {
            let item = this.elements[key];
            if (item instanceof Choices) {
                let sel = item.passedElement.element;
                sel.addEventListener('change', (e) => {
                    this.handleValidate(sel);
                });
            } else {
                item.addEventListener('input', (e) => {
                    this.handleValidate(item);
                });
            }
        }

    }

    handleValidate(element) {
        let name = element.getAttribute('name');
        let validate = this.validate[name] ?? [];
        let values = this.value().get()[name] ?? null;
        let messages = []
        if (name && validate.length > 0) {
            for (let vl of validate) {
                let arr = vl.split(":");
                let validatorType = arr[0];
                let set = arr[1];
                if (set) {
                    let err = Validator[validatorType](values,set);
                    if(err !== ''){
                        messages.push(err);
                    }
                } else {
                    let err = Validator[validatorType](values);
                    if(err !== ''){
                        messages.push(err);
                    }
                }
            }
        }
        this.errors[name] = {
            ...this.errors[name],
            messages
        };
        return this.showValidate(name);
    }
    showValidate(key){
        let { attribute, messages } = this.errors[key];
        let ele = this.elements[key];
        if(ele instanceof Choices){
            ele = ele.passedElement.element
        }
        let mess = '';
        let show = false;
        if(messages.length > 0){
            show = true;
            mess = `${attribute} ${messages[0]}`;
        }
        this.changeValidateMessage(ele,show,mess)
        return show;
    }

    changeValidateMessage(
        element,
        error = false,
        message = "",
        listClass = ["p-2", "small"]
    ) {
        if (!element || !(element instanceof HTMLElement)) return;

        const isChoicesSelect = element.tagName.toLowerCase() === "select" && element.hasAttribute('data-choice');
        if (isChoicesSelect) {
            element = element.parentNode.parentNode;
        }
        let parentNode = element.parentNode;
    
        let classError = "show-error";
        let errorElement = parentNode.querySelector(`.${classError}`);
    
        if (error) {
            message = capitalizeFirstLetter(message);
            message = message.charAt(0).toUpperCase() + message.slice(1).toLowerCase();
            if (errorElement) {
                errorElement.innerHTML = message;
            } else {
                errorElement = document.createElement("div");
                errorElement.classList.add(classError, "text-danger", ...listClass);
                errorElement.innerHTML = message;
                parentNode.appendChild(errorElement);
            }
        } else if (errorElement) {
            parentNode.removeChild(errorElement);
        }
        changeClassValidate(element, error, isChoicesSelect);
        return message;
    }

    checkValidate() {
        let err = true;
        for (let key in this.elements) {
            let item = this.elements[key];
            if(item instanceof Choices){
                item = item.passedElement.element
            }
            let check = this.handleValidate(item);
            if(check) err = false;
        }
        return err;
    }

    removeCommas(numberString) {
        const cleanedString = numberString.replace(/,/g, "");
        const number = parseInt(cleanedString, 10);
        return number;
    };

    dateTimeFormat(date, format = "d-m-Y") {
        let currentDate;
        if (date == "0000-00-00 00:00:00" || date == "0000-00-00" || date == "") {
            return "";
        }
        if (typeof date === "string" || typeof date === "number") {
            currentDate = new Date(date);
        } else {
            return "";
        }

        let seconds = currentDate.getSeconds().toString().padStart(2, "0"); // Add leading zero if needed
        let minutes = currentDate.getMinutes().toString().padStart(2, "0"); // Add leading zero if needed
        let hours = currentDate.getHours().toString().padStart(2, "0"); // Add leading zero if needed
        let day = currentDate.getDate().toString().padStart(2, "0"); // Add leading zero if needed
        let month = (currentDate.getMonth() + 1).toString().padStart(2, "0"); // Month is zero-based
        let year = currentDate.getFullYear();
        let result = format.replace("i", minutes);
        result = result.replace("s", seconds);
        result = result.replace("H", hours);
        result = result.replace("d", day);
        result = result.replace("m", month);
        result = result.replace("Y", year);
        return result;
    };

    formatNumber(numberString, max = 0, groupSeparator = ',', decimalSeparator = '.') {
        const number = parseFloat(numberString);
        if (isNaN(number)) {
            throw new Error("Invalid number string");
        }
        const options = {
            minimumFractionDigits: 0,
            maximumFractionDigits: max,
            useGrouping: true,
        };
        const formattedNumber = number.toLocaleString("en-US", options);

        const customFormattedNumber = formattedNumber
            .replace(/,/g, groupSeparator)
            .replace(/\./g, decimalSeparator);

        return customFormattedNumber;
    };

    // Lấy data 
    value() {
        let data = {};
        for (let key in this.elements) {
            let item = this.elements[key];
            if (item instanceof Choices) {
                let sel = item.passedElement.element;
                if (sel.hasAttribute("multiple")) {
                    data[key] = item?.getValue()?.map(choice => choice.value) ?? [];
                } else {
                    data[key] = sel.value;
                }
            } else {
                data[key] = item.value;
            }
        }
        this.data = data;
        return this;
    }

    // Lấy value
    get() {
        return this.data;
    }

    // Hiển thị lỗi ra form
    logError(errors) {
        for (let name in errors) {
            let ele = this.form.querySelector(`[name="${name}"]`);
            if (ele) {
                if (ele.tagName.toLowerCase() == "select") {
                    let checkChoice = ele.hasAttribute("data-choice");
                    changeValidateMessage(ele, true, errors[name][0], ["p-2", "small"], checkChoice);
                } else {
                    changeValidateMessage(ele, true, errors[name][0]);
                }
            }
        }
    }

    // Khởi tạo danh sách element
    iniElement() {
        let listElements = [...this.form.querySelectorAll("select, textarea, input, button, fieldset, legend, output, [type='radio'], [type='checkbox']")];
        let data = listElements.reduce((acc, item) => {
            if (item.tagName.toLowerCase() === 'select') {
                acc[item.name] = new Choices(item, choiceOption);
            } else {
                acc[item.name] = item;
            }
            return acc;
        }, {});
        this.elements = data;
    }

    // Show dữ liệu ra form
    showValue(value, format = { price: [], date: [] }) {
        format.date = format.date || [];
        format.price = format.price || [];
        for (let name in value) {
            let ele = this.form.querySelector(`[name="${name}"]`);
            if (ele) {
                if (ele.tagName.toLowerCase() == "select") {
                    let checkChoice = ele.hasAttribute("data-choice");
                    if (checkChoice) {
                        let dataSet = value[name];
                        if (ele.hasAttribute("multiple")) {
                            dataSet = dataSet.map(item => {
                                return String(item);
                            })
                        } else {
                            dataSet = String(dataSet);
                        }
                        this.elements[name].setChoiceByValue(dataSet);
                    } else {
                        ele.value = value[name];
                    }
                } else {
                    if (format.price.includes(name)) {
                        ele.value = value[name] ? this.formatNumber(value[name]) : 0;
                    } else if (format.date.includes(name)) {
                        ele.value = this.dateTimeFormat(value[name], 'd-m-Y');
                    } else {
                        ele.value = value[name];
                    }
                }
            }
        }

    }

    // Format tiền tệ
    formatPrice(array = []) {
        for (let name in this.data) {
            if (array.includes(name)) {
                let value = this.removeCommas(this.data[name]);
                this.data[name] = isNaN(value) ? '' : value;
            }
        }
        return this;
    }

    // Thực thi
    execute() {
        this.form.addEventListener("submit", (e) => this.submit(e));
    }
}

class HandleForm extends Form {
    modal = null;
    modalBT = null;
    form = null;
    constructor(modal) {
        super();
        this.modal = document.querySelector(modal);
        this.form = this.modal.querySelector("form");
        this.modalBT = new bootstrap.Modal(this.modal);
        this.iniElement();
        this.setValidate();
        this.execute();
    }
    closeReset() {
        this.modal.addEventListener('hide.bs.modal', () => {
            this.reset();
        });
    }
    setBackModal(modal) {
        let btnBack = this.form.querySelector(".btn-prev-modal");
        if (btnBack) {
            btnBack.addEventListener("click", () => {
                this.hideModal();
                modal.showModal();
            });
        }
    }
    loading(type = false, text = '') {
        btnLoading(this.form.querySelector("button[type='submit']"), type, text);
    }
    redirectMD(url) {
        let modal = document.getElementById("modalSuccessNotification");
        modal.addEventListener('hide.bs.modal', function () {
            window.location.href = url;
        });
    }
    hideModal() {
        this.modalBT.hide();
    }
    showModal() {
        this.modalBT.show();
    }

}

class File {
    /**
     * Hàm xuất file excel.
     * 
     * @param {btn} element Button của thẻ muốn làm hiệu ứng loading
     * @param {Config} {
     *      route: 'đường dẫn tới api xử lý',
     *      method: 'method của route - mặc định POST',
     *      filename: 'Tên của file',
     *      btnText: 'Text của btn khi loading'
     *      data: {} Data của bản muốn đẩy lên để lọc - nếu có
     * } 
     * @returns {number} Số ngày giữa hai ngày
     */
    static async export(btn, paramConfig = {}) {
        const defaultConfig = {
            route: '',
            method: 'POST',
            filename: 'filename',
            btnText: '',
            data: {},
        };
        const mergedConfig = Object.assign({}, defaultConfig, paramConfig);

        let config = {
            method: mergedConfig.method,
            url: mergedConfig.route,
            data: mergedConfig.data,
            responseType: "blob",
        };

        btnLoading(btn, true, mergedConfig.btnText);
        try {
            let fetch = await axios(config).then((res) => res);
            const url = window.URL.createObjectURL(new Blob([fetch.data]));
            const link = document.createElement("a");
            link.href = url;
            link.setAttribute("download", mergedConfig.filename + ".xlsx"); // Tên file tải về
            document.body.appendChild(link);
            link.click();
            link.parentNode.removeChild(link);
        } catch (error) {
            showErrorMD('Đã xảy ra lỗi, vui lòng thử lại sau!');
        }
        btnLoading(btn, false, mergedConfig.btnText);
    }
}



class RequestServer {
    constructor(route) {
        this.index = 1;
        this.route = route;
        this.response = null;
        this.colspan = 5;
        this.id = 0;
        this.tbody = "#data_table_body";
        this.paginations = ".paginations";
        this.content = "";
        this.init = false;
        this.params = {};
        this.totalContent = null;
        this.insert = () => { };
    }

    bold(id) {
        return this.id == id ? 'tr-bold' : '';
    }
    async get(url = "") {
        let links = url === "" ? this.route : `${url}`;

        let params = {};
        if (!this.init) {
            params = this.getParams();
        } else {
            params = this.params;
        }
        for (let i in params) {
            if (typeof params[i] === 'string') {
                if (params[i].trim() === '') {
                    delete params[i];
                }
            }
        }

        try {
            let response = await axios.get(links, { params }).then(res => res);
            if (response.status === 200) {
                this.index = response.data.from;
                this.response = response.data;
                this.setParams(response.data);
                this.showData();
                this.id = 0;
                this.init = true;
            }
        } catch (error) {
            console.log(error);
        }
    }

    setLabel() {
        let tbodyElement = document.querySelector(this.tbody);
        let tableElement = tbodyElement.closest('table');
        if (tableElement) {
            tableElement.classList.add('table-config');
            let headers = tableElement.querySelectorAll('thead th');
            let rows = tableElement.querySelectorAll('tbody tr');
            rows.forEach(function (row) {
                if (!row.classList.contains('none-data')) {
                    let cells = row.querySelectorAll('td');
                    cells.forEach(function (cell, index) {
                        let label = headers[index].textContent.trim();
                        label = label.toUpperCase();
                        cell.setAttribute('data-label', label);
                    });
                }
            });
        }
    }

    getParams(query = '') {
        var searchParams = null;
        if (query === '') {
            searchParams = new URLSearchParams(window.location.search);
        } else {
            searchParams = new URLSearchParams(query);
        }
        searchParams = [...searchParams];
        let params = searchParams.reduce((acc, item) => {
            if (item[0].endsWith('[]')) {
                let key = item[0].slice(0, -2);
                if (!acc[key]) {
                    acc[key] = [];
                }
                acc[key].push(item[1]);
            } else {
                acc[item[0]] = item[1];
            }
            return acc;
        }, {});
        return params;
    }

    reset() {
        this.params = {};
        this.get(this.route);
    }

    setParams(data) {
        const urlParams = new URLSearchParams(data.params);

        const page = urlParams.get('page');
        if (page == 1) {
            urlParams.delete('page');
        }

        let url = new URL(data.url + '?' + urlParams.toString());
        this.params = this.getParams(data.params);
        const newUrl = `${window.location.protocol}//${window.location.host}${window.location.pathname}${url.search}`;
        window.history.replaceState({ path: newUrl }, '', newUrl);
    }

    setCookie(data) {
        console.log(data);
    }

    showData() {
        let data = this.response.data;
        this.content = this.insert(data);
        let contentLoading = "";
        if (data.length <= 0) {
            contentLoading = `<tr><td colspan="${this.colspan}" class="text-center fw-bold fs-7 text-danger">Chưa có dữ liệu</td></tr>`;
            document.querySelector(this.tbody).innerHTML = contentLoading;
        } else {
            document.querySelector(this.tbody).innerHTML = this.content;
            this.setLabel();
        }

        let paginations = document.querySelector(this.paginations);
        this.setPaginations(this.response, paginations);
    }

    setPaginations = (data, element) => {
        if (this.totalContent) {
            this.totalContent.textContent = data.total;
        }
        let pathHere = new URL(data.url + data.params);
        pathHere.searchParams.get('page');
        let pathALl = pathHere.toString();
        pathHere.searchParams.delete('show_all');
        let pathNotALl = pathHere.toString();
        let html = `<div class="row align-items-center justify-content-between py-2 pe-0 fs-9">
            <div class="col-auto d-flex">
                <p class="mb-0 d-none d-sm-block me-3 fw-semibold text-body">
                ${data.from} đến ${data.to}<span class="text-body-tertiary"> Trong </span> ${data.total}
                </p>
                <a class="btn-link" href="javascript:" title="Tất cả" ${data.all ? "hidden" : ""
            } data-pagelinks="${pathALl + "&show_all=true"
            }">Tất cả<span class="fas fa-angle-right ms-1"></span></a>
                <a class="btn-link" href="javascript:" title="Thu gọn" ${data.all ? "" : "hidden"
            } data-pagelinks="${pathNotALl}">
                    Thu gọn<span class="fas fa-angle-left ms-1"></span>
                </a>
            </div>
                `;
        if (!data.all) {
            let urlNP = new URL(data.url + data.params);
            urlNP.searchParams.set('page', parseInt(data.currentPage) - 1);
            let prePage = urlNP.toString();
            urlNP.searchParams.set('page', parseInt(data.currentPage) + 1);
            let nextPage = urlNP.toString();
            html += `
                <nav class="col-auto d-flex">
                    <ul class="mb-0 pagination justify-content-end">
                        <li class="page-item ${data.currentPage <= 1 ? "disabled" : ""
                }">
                            <a class="page-link ${data.currentPage <= 1 ? "disabled" : ""
                }" ${data.currentPage <= 1 ? 'disabled=""' : ""
                } href="javascript:" title="Trang trước" data-pagelinks="${prePage.toString()}">
                                <span class="fas fa-chevron-left"></span>
                            </a>
                        </li>`;
            html += getPage(data);
            html += `
                <li class="page-item ${data.currentPage >= data.totalPages ? "disabled" : ""
                }">
                            <a class= "page-link ${data.currentPage >= data.totalPages ? "disabled" : ""
                }"  href="javascript:" title="Trang sau"  data-pagelinks="${nextPage.toString()
                }" >
                            <span class= "fas fa-chevron-right"></span>
                            </a>
                        </li>
                    </ul>
                </nav>
                `;
        }
        html += `
            </div>
            `;
        if (element) {
            element.innerHTML = html;
        }

        function getPage(data) {
            let html = "";
            let start = +data.currentPage - 3;
            let max = +data.currentPage + 3;

            if (start > 1) {
                html += `<li class="page-item disabled"><a class="page-link" disabled="" title="" type="button" href="javascript:">...</a>`;
            }

            for (let index = start; index <= max; index++) {
                if (index > 0 && index <= +data.totalPages) {
                    if (index == +data.currentPage) {
                        html += `<li class="page-item active"><a class="page-link" title="Trang ${index}" href="javascript:" type="button">${index}</a></li>`;
                    } else {
                        let pathUrl = new URL(data.url + data.params);
                        pathUrl.searchParams.set('page', index);
                        html += `<li class="page-item"><a class="page-link" type="button" title="Trang ${index}" href="javascript:" data-pagelinks="${pathUrl.toString()}">${index}</a></li>`;
                    }
                }
            }
            if (max < +data.totalPages) {
                html += `<li class="page-item disabled"><a class="page-link" disabled="" title="" type="button" href="javascript:">...</a></li>`;
            }
            return html;
        }

        if (element) {
            let pageLinks = element.querySelectorAll("a[data-pageLinks]");
            pageLinks.forEach((link) => {
                link.addEventListener("click", async () => {
                    btnLoading(link, true, link.textContent);
                    let pageLinks = link.getAttribute("data-pageLinks");
                    this.params = {};
                    await this.get(pageLinks);
                    btnLoading(link, false, link.textContent);
                });
            });
        }
    };
}

class HandleConfirm {

    success = () => { };

    config = {
        text: 'Bạn có chắc chắn muốn xóa không?',
        btnText: 'Xóa',
        btnBg: 'red',
    }

    loading(type = false, text = '') {
        btnLoading(this.btnConfirm, type, text);
    }


    constructor() {
        this.modal = document.getElementById("modalConfirmDelete");
        this.btnConfirm = this.modal.getElementsByClassName("btn-confirm")[0];
        this.modalBT = new bootstrap.Modal(this.modal, { keyboard: false });
        this.element = this.modal.getElementsByClassName("confirm-message")[0];
        this.btnConfirm.addEventListener("click", (e) => { this.success(e) });
    }

    hide() {
        this.modalBT.hide();
    }

    show() {
        this.btnConfirm.style.backgroundColor = this.config.btnBg;
        this.element.innerHTML = this.config.text;
        this.btnConfirm.textContent = this.config.btnText;
        this.modalBT.show();
    }

}


class Status {
    static up(up) {
        if (!!up) {
            return `<span class='badge fs-10 bg-primary-subtle text-primary-emphasis'>Đã đăng</span>`;
        }
        return `<span class='badge fs-10 bg-warning-subtle text-warning-emphasis'>Chưa đăng</span>`;
    }
}


