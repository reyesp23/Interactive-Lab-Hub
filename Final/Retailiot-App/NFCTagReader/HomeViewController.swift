//
//  HomeViewController.swift
//  SmartRack
//
//  Created by Patricio Reyes on 25/11/21.
//  Copyright © 2021 Patricio. All rights reserved.
//

import UIKit
import CoreNFC
import SceneKit

class HomeViewController: UIViewController {
        
    @IBOutlet weak var lockButton: UIButton! {
        didSet {
            lockButton.isHidden = true
        }
    }
    
    @IBOutlet weak var scanButton: UIButton! {
        didSet {
            scanButton.tintColor = .white
            scanButton.setTitleColor(.lightGray, for: .disabled)
            scanButton.setTitleColor(.white, for: .normal)
            scanButton.backgroundColor = .systemBlue
            scanButton.layer.cornerRadius = 12
            scanButton.titleLabel?.font = UIFont.systemFont(ofSize: 17, weight: .bold)
            scanButton.setTitle("Scan", for: .normal)
        }
    }
    
    // MARK: - Properties
    var session: NFCNDEFReaderSession?
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        // Initialize Tap Gesture Recognizer
          let tapGestureRecognizer = UITapGestureRecognizer(target: self, action: #selector(didTapView))

          // Configure Tap Gesture Recognizer
          tapGestureRecognizer.numberOfTapsRequired = 2

          // Add Tap Gesture Recognizer
          view.addGestureRecognizer(tapGestureRecognizer)
    }
    
    @objc func didTapView(_ sender: UITapGestureRecognizer) {
        lockButton.isHidden = !lockButton.isHidden
    }
        
    // MARK: - Actions
    @IBAction func scanPressed(_ sender: Any) {
        initNFCSession()
    }
    
    func showItemDetail(id: String) {
        let storyboard = UIStoryboard(name: "Main", bundle: .main)
        guard let vc = storyboard.instantiateViewController(withIdentifier: "ItemDetailViewControllerID") as? ItemDetailViewController else { return }
        
   
        switch id {
        case "a":
            let product = Product.crewNeck
            vc.product = product
        case "b":
            let product = Product.basicShirt
            vc.product = product
        case "c":
            let product = Product.denimShirt
            vc.product = product
        default: break
        }
        
        self.present(vc, animated: true)
    }
    
    func initNFCSession() {
        guard NFCNDEFReaderSession.readingAvailable else {
            let alertController = UIAlertController(
                title: "Scanning Not Supported",
                message: "This device doesn't support tag scanning.",
                preferredStyle: .alert
            )
            alertController.addAction(UIAlertAction(title: "OK", style: .default, handler: nil))
            self.present(alertController, animated: true, completion: nil)
            return
        }
        
        session = NFCNDEFReaderSession(delegate: self, queue: nil, invalidateAfterFirstRead: false)
        session?.alertMessage = "Hold your iPhone near the tag to scan product"
        session?.begin()
    }
    @IBAction func lockButtonPressed(_ sender: Any) {
        lockRequest()
    }
}

extension HomeViewController {
    
    
    func lockRequest() {
        
        let url = url(with: "123", state: 1)
        guard let request = createRequest(with: url,
                                          cachePolicy: .reloadIgnoringLocalAndRemoteCacheData,
                                          timeout: 50 ) else { return }
        
        URLSession.shared.dataTask(with: request) { [weak self] (data: Data?, response: URLResponse?, error: Error?) in
          
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
