//
//  ItemDetailViewController.swift
//  NFCTagReader
//
//  Created by Patricio Reyes on 30/11/21.
//  Copyright © 2021 Apple. All rights reserved.
//

import UIKit
import PassKit

class ItemDetailViewController: UIViewController {
    
    var id: String?
    var product: Product = Product.crewNeck
    
    let paymentHandler = PaymentHandler()

        
    @IBOutlet weak var colourView: UIView! {
        didSet{
            colourView.backgroundColor = product.color.color
            colourView.layer.cornerRadius = colourView.bounds.height/2
        }
    }
    
    @IBOutlet weak var sizeView: UIView! {
        didSet {
            sizeView.backgroundColor  = .clear
            sizeView.layer.cornerRadius = 7
            sizeView.layer.borderWidth = 3
            sizeView.alpha = 0.8

            sizeView.layer.borderColor = UIColor.lightGray.cgColor
        }
    }
    
    
    @IBOutlet weak var titleLabel: UILabel! {
        didSet{
            titleLabel.text = product.name
        }
    }
    @IBOutlet weak var imageView: UIImageView!{
        didSet {
            imageView.image = product.image
        }
    }
    
    @IBOutlet weak var colorLabel: UILabel! {
        didSet {
            colorLabel.text = product.color.description
        }
    }
    
    @IBOutlet weak var sizeLabel: UILabel! {
        didSet {
            sizeLabel.text = product.size.description
        }
    }
    
    @IBOutlet weak var sizeIcon: UILabel! {
        didSet {
            sizeIcon.text = product.size.initial
        }
    }
    
    @IBOutlet weak var priceLabel: UILabel! {
        didSet {
            priceLabel.text = "$\(product.price)"
        }
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
                
        let button = PKPaymentButton(paymentButtonType: .plain, paymentButtonStyle: .black)
        button.addTarget(self, action: #selector(applePay), for: .touchUpInside)
        button.titleLabel?.font = UIFont.systemFont(ofSize: 12, weight: .bold)
        button.cornerRadius = 12
        
        let secondButton = UIButton()
        secondButton.tintColor = .white
        secondButton.setTitleColor(.lightGray, for: .disabled)
        secondButton.setTitleColor(.white, for: .normal)
        secondButton.backgroundColor = .systemBlue
        secondButton.layer.cornerRadius = 12
        secondButton.titleLabel?.font = UIFont.systemFont(ofSize: 20, weight: .bold)
        secondButton.setTitle("Buy", for: .normal)
        secondButton.addTarget(self, action: #selector(payButtonPressed), for: .touchUpInside)


        let constraints = [
            button.trailingAnchor.constraint(equalTo: view.layoutMarginsGuide.trailingAnchor),
            button.bottomAnchor.constraint(equalTo: view.layoutMarginsGuide.bottomAnchor),
            button.heightAnchor.constraint(equalToConstant: 50),
            button.widthAnchor.constraint(equalToConstant: 163),
            
            secondButton.leadingAnchor.constraint(equalTo: view.layoutMarginsGuide.leadingAnchor),
            secondButton.bottomAnchor.constraint(equalTo: view.layoutMarginsGuide.bottomAnchor),
            secondButton.heightAnchor.constraint(equalToConstant: 50),
            secondButton.widthAnchor.constraint(equalToConstant: 163)

        ]
        button.translatesAutoresizingMaskIntoConstraints = false
        secondButton.translatesAutoresizingMaskIntoConstraints = false
        view.addSubview(button)
        view.addSubview(secondButton)
        NSLayoutConstraint.activate(constraints)
    }
    
    @objc func payButtonPressed(_ sender: Any) {
        sendRequest()
    }
    
    @objc func applePay(_ sender: Any) {
        paymentHandler.startPayment(amount: product.price) { (success) in
            if success {
                self.dismiss(animated: true, completion: nil)
            }
        }
    }
    
    func sendRequest() {
        let url = url(with: id ?? "", state: 0)
        guard let request = createRequest(with: url,
                                          cachePolicy: .reloadIgnoringLocalAndRemoteCacheData,
                                          timeout: 50 ) else { return }
        
        URLSession.shared.dataTask(with: request) { [weak self] (data: Data?, response: URLResponse?, error: Error?) in
            DispatchQueue.main.async {
                self?.dismiss(animated: true, completion: nil)
            }
        }.resume()
    }
    
    private func url(with id: String, state: Int) -> URL? {
        return URL(string: "https://smart-clothes-lock.herokuapp.com/toggle/\(id)/\(state)")
    }
    
    func createRequest(with url: URL?, cachePolicy: URLRequest.CachePolicy, timeout: Double) -> URLRequest? {
       
        if let url = url{
            var request = URLRequest(url:url)
            request.httpMethod = "GET"
            request.cachePolicy = cachePolicy
            request.timeoutInterval = timeout
            return request
        }else {return nil}
        
    }
}
